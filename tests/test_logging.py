"""Functional tests for the logger module."""

import json

import pytest
from pytest import LogCaptureFixture, MonkeyPatch

from ai_base_template.logging import (
    bind_contextvars,
    clear_context_fields,
    configure_structlog,
    get_correlation_id,
    get_logger,
)


@pytest.fixture(autouse=True)
def setup_logger():
    """Configure logger before each test and clean up after."""
    configure_structlog()
    yield
    clear_context_fields()


# Correlation ID Functionality Tests


def test_correlation_id_appears_in_logged_json(caplog: LogCaptureFixture) -> None:
    """Verify correlation_id is preserved in JSON log output for request tracing."""
    # Bind a correlation ID as would happen at request start
    correlation_id = "req-abc-123"
    bind_contextvars(correlation_id=correlation_id)

    # Log a message as would happen during request processing
    logger = get_logger("api_handler")
    logger.info("Processing request")

    # Parse the JSON output
    log_output = json.loads(caplog.records[0].message)

    # Verify correlation_id is in the extra fields
    assert "extra" in log_output
    assert log_output["extra"]["correlation_id"] == correlation_id


def test_get_correlation_id_returns_unknown_when_unset() -> None:
    """Ensure get_correlation_id provides safe fallback when ID is not bound."""
    # Don't bind any correlation_id
    clear_context_fields()

    # Should return "unknown" as default
    assert get_correlation_id() == "unknown"


def test_get_correlation_id_retrieves_bound_value() -> None:
    """Verify get_correlation_id returns the bound correlation ID."""
    correlation_id = "test-correlation-456"
    bind_contextvars(correlation_id=correlation_id)

    assert get_correlation_id() == correlation_id


# Log Output Structure Tests


def test_logger_outputs_valid_json_structure(caplog: LogCaptureFixture) -> None:
    """Ensure log output is valid JSON with required fields for log processors."""
    logger = get_logger("test_logger")
    logger.info("Test message", custom_field="custom_value")

    # Should be valid JSON
    log_output = json.loads(caplog.records[0].message)

    # Verify required fields exist
    assert "timestamp" in log_output
    assert "level" in log_output
    assert "logger" in log_output
    assert "message" in log_output
    assert log_output["message"] == "Test message"
    assert log_output["logger"] == "test_logger"
    assert log_output["level"] == "info"


def test_custom_fields_isolated_in_extra_dict(caplog: LogCaptureFixture) -> None:
    """Verify custom fields are isolated to prevent field name collisions."""
    logger = get_logger("api")

    # Log with custom fields
    logger.info("API call", user_id="user-123", endpoint="/api/v1/chat", method="POST", status_code=200)

    log_output = json.loads(caplog.records[0].message)

    # Standard fields should be at root level
    assert "timestamp" in log_output
    assert "level" in log_output
    assert "message" in log_output
    assert "logger" in log_output
    assert "context" in log_output

    # Custom fields should be in extra
    assert "extra" in log_output
    assert log_output["extra"]["user_id"] == "user-123"
    assert log_output["extra"]["endpoint"] == "/api/v1/chat"
    assert log_output["extra"]["method"] == "POST"
    assert log_output["extra"]["status_code"] == 200

    # Verify standard fields are not in extra
    assert "timestamp" not in log_output["extra"]
    assert "level" not in log_output["extra"]
    assert "message" not in log_output["extra"]


# Log Level Filtering Tests


def test_logging_level_filters_messages(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Verify log level setting correctly filters messages for production log control."""
    # Set INFO level
    monkeypatch.setenv("LOGGING_LEVEL", "INFO")
    configure_structlog()

    logger = get_logger("test")

    # Log at different levels
    logger.debug("Debug message - should not appear")
    logger.info("Info message - should appear")
    logger.warning("Warning message - should appear")
    logger.error("Error message - should appear")

    # Only INFO and above should be logged
    messages = [json.loads(record.message)["message"] for record in caplog.records]

    assert "Debug message - should not appear" not in messages
    assert "Info message - should appear" in messages
    assert "Warning message - should appear" in messages
    assert "Error message - should appear" in messages


def test_invalid_log_level_defaults_to_info(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Ensure invalid log level falls back to INFO safely."""
    # Set invalid level
    monkeypatch.setenv("LOGGING_LEVEL", "INVALID")
    configure_structlog()

    logger = get_logger("test")

    # Should still work with INFO level
    logger.debug("Should not appear")
    logger.info("Should appear")

    messages = [json.loads(record.message)["message"] for record in caplog.records]
    assert "Should not appear" not in messages
    assert "Should appear" in messages


# Context Isolation Tests


def test_context_clears_between_requests(caplog: LogCaptureFixture) -> None:
    """Verify context clearing prevents data leakage between requests."""
    logger = get_logger("request_handler")

    # First request
    bind_contextvars(correlation_id="request-1", user_id="user-1")
    logger.info("Processing first request")

    # Clear context as would happen at request end
    clear_context_fields()

    # Second request - should not have first request's context
    bind_contextvars(correlation_id="request-2")  # Note: no user_id
    logger.info("Processing second request")

    # Parse both logs
    first_log = json.loads(caplog.records[0].message)
    second_log = json.loads(caplog.records[1].message)

    # First log should have both fields
    assert first_log["extra"]["correlation_id"] == "request-1"
    assert first_log["extra"]["user_id"] == "user-1"

    # Second log should only have correlation_id, not user_id
    assert second_log["extra"]["correlation_id"] == "request-2"
    assert "user_id" not in second_log.get("extra", {})


def test_correlation_id_propagates_through_request_lifecycle(caplog: LogCaptureFixture) -> None:
    """Verify correlation_id propagates through entire request without re-binding."""
    # Bind correlation_id once at request start
    correlation_id = "request-lifecycle-789"
    bind_contextvars(correlation_id=correlation_id)

    # Simulate multiple log points in request processing
    logger1 = get_logger("auth")
    logger1.info("Authenticating user")

    logger2 = get_logger("database")
    logger2.info("Querying database")

    logger3 = get_logger("response")
    logger3.info("Sending response")

    # All logs should have the same correlation_id
    for record in caplog.records:
        log_output = json.loads(record.message)
        assert log_output["extra"]["correlation_id"] == correlation_id


# Critical Safety Tests for New Logging Features


def test_testing_mode_produces_human_readable_output(caplog: LogCaptureFixture) -> None:
    """End-to-end test that TESTING=True actually produces human-readable logs."""
    # Configure logger in testing mode
    configure_structlog(testing=True)

    # Bind context and log with extra fields
    bind_contextvars(correlation_id="test-123-abc")
    logger = get_logger("core.chat")
    logger.info("Processing user query", query="How many customers?", duration_ms=150, status_code=200)

    # Should get human-readable format, not JSON
    log_output = caplog.records[0].message

    # Verify it's NOT JSON (would raise exception if we tried to parse)
    with pytest.raises((json.JSONDecodeError, ValueError)):
        json.loads(log_output)

    # Verify human-readable format components
    assert "[INFO]" in log_output
    assert "core.chat:" in log_output
    assert "Processing user query" in log_output
    assert "query=How many customers?" in log_output
    assert "150ms" in log_output
    assert "HTTP 200" in log_output
    assert "[id:test-123]" in log_output  # Truncated correlation ID


def test_production_mode_still_produces_json_output(caplog: LogCaptureFixture) -> None:
    """Ensure existing JSON logging unaffected by new features."""
    # Configure logger in production mode (default)
    configure_structlog(testing=False)

    # Bind context and log with extra fields
    bind_contextvars(correlation_id="prod-456-def")
    logger = get_logger("api.handler")
    logger.info("Processing request", user_id="user-123", endpoint="/api/chat")

    # Should be valid JSON
    log_output = json.loads(caplog.records[0].message)

    # Verify JSON structure matches existing format
    assert "timestamp" in log_output
    assert "level" in log_output
    assert "logger" in log_output
    assert "message" in log_output
    assert "context" in log_output
    assert "extra" in log_output

    # Verify content
    assert log_output["level"] == "info"
    assert log_output["logger"] == "api.handler"
    assert log_output["message"] == "Processing request"
    assert log_output["extra"]["correlation_id"] == "prod-456-def"
    assert log_output["extra"]["user_id"] == "user-123"
    assert log_output["extra"]["endpoint"] == "/api/chat"


def test_human_readable_renderer_formats_complete_log_entry(caplog: LogCaptureFixture) -> None:
    """HumanReadableRenderer should format all components correctly."""
    configure_structlog(testing=True)

    # Bind correlation ID and log with full context
    bind_contextvars(correlation_id="complete-test-789")
    logger = get_logger("ai_sql_assistant.services.llm.session")
    logger.warning("LLM call completed", duration_ms=2500, status_code=200, model="gpt-4o-mini")

    log_output = caplog.records[0].message

    # Verify format: "HH:MM:SS [LEVEL] logger: message [key_info] [correlation_id]"
    assert "[WARNING]" in log_output
    assert "llm.session:" in log_output  # Should be abbreviated
    assert "LLM call completed" in log_output
    assert "2500ms" in log_output
    assert "HTTP 200" in log_output
    assert "model=gpt-4o-mini" in log_output
    assert "[id:complete]" in log_output  # Truncated to 8 chars

    # Verify timestamp format (HH:MM:SS at start)
    import re

    timestamp_pattern = r"^\d{2}:\d{2}:\d{2}"
    assert re.match(timestamp_pattern, log_output)


def test_human_readable_renderer_handles_empty_fields(caplog: LogCaptureFixture) -> None:
    """Renderer should handle missing/empty fields gracefully."""
    configure_structlog(testing=True)

    # Log without correlation ID or extra fields
    logger = get_logger("simple.logger")
    logger.error("Simple error message")

    log_output = caplog.records[0].message

    # Should not crash and should format basic components
    assert "[ERROR]" in log_output
    assert "simple.logger:" in log_output
    assert "Simple error message" in log_output

    # Should not have extra brackets or correlation ID
    assert "[id:" not in log_output
    assert "[]" not in log_output


def test_abbreviate_logger_name_shortens_project_loggers() -> None:
    """Project logger names should be abbreviated for readability."""
    from ai_base_template.logging import _abbreviate_logger_name

    # Test project logger abbreviation
    assert _abbreviate_logger_name("ai_base_template.core.chat") == "core.chat"
    assert _abbreviate_logger_name("ai_base_template.services.llm.session") == "llm.session"
    assert _abbreviate_logger_name("ai_base_template.middleware.logger") == "middleware.logger"
    assert _abbreviate_logger_name("ai_base_template.api.threads") == "api.threads"

    # Test single component (should use last part)
    assert _abbreviate_logger_name("ai_base_template.main") == "main"

    # Test external loggers (should be unchanged)
    assert _abbreviate_logger_name("werkzeug") == "werkzeug"
    assert _abbreviate_logger_name("sqlalchemy.engine") == "sqlalchemy.engine"
    assert _abbreviate_logger_name("litellm") == "litellm"


def test_format_extra_fields_prioritizes_important_fields() -> None:
    """Important fields like status_code, duration_ms should appear first."""
    from ai_base_template.logging import _format_extra_fields

    # Test with mix of important and regular fields
    extra = {
        "user_id": "user-123",
        "status_code": 200,
        "request_type": "chat",
        "duration_ms": 1500,
        "endpoint": "/api/v1/chat",
        "response_size_bytes": 2048,
    }

    result = _format_extra_fields(extra)

    # Should start with brackets
    assert result.startswith(" [")
    assert result.endswith("]")

    # Important fields should appear first in specific format
    content = result[2:-1]  # Remove " [" and "]"
    fields = [f.strip() for f in content.split(",")]

    # Check that important fields are formatted specially and appear early
    important_fields_found = []
    for field in fields[:4]:  # Check first 4 fields
        if "HTTP" in field:
            important_fields_found.append("status_code")
        elif "ms" in field and "=" not in field:  # Duration without "=" means special format
            important_fields_found.append("duration_ms")
        elif "B" in field and "=" not in field:  # Bytes without "=" means special format
            important_fields_found.append("response_size_bytes")

    # At least status_code and duration_ms should be in special format
    assert "status_code" in important_fields_found
    assert "duration_ms" in important_fields_found

    # Regular fields should have key=value format
    assert any("user_id=user-123" in field for field in fields)


def test_correlation_id_works_in_human_readable_mode(caplog: LogCaptureFixture) -> None:
    """Correlation IDs should work in human-readable format."""
    configure_structlog(testing=True)

    # Test with long correlation ID (should be truncated)
    long_correlation_id = "very-long-correlation-id-that-should-be-truncated-123456789"
    bind_contextvars(correlation_id=long_correlation_id)

    logger = get_logger("correlation.test")
    logger.info("Test correlation ID display")

    log_output = caplog.records[0].message

    # Should appear as truncated correlation ID
    assert "[id:very-lon]" in log_output  # First 8 characters

    # Should not contain the full correlation ID
    assert long_correlation_id not in log_output

    # Test with shorter correlation ID
    clear_context_fields()
    bind_contextvars(correlation_id="short")
    logger.info("Test short correlation ID")

    log_output = caplog.records[1].message
    assert "[id:short]" in log_output


def test_configure_structlog_chooses_correct_renderer() -> None:
    """configure_structlog should choose renderer based on testing flag."""
    import structlog

    # Test production mode - should use JSONRenderer
    configure_structlog(testing=False)
    config = structlog.get_config()

    # Check that JSONRenderer is in processors
    renderer_types = [type(processor).__name__ for processor in config["processors"]]
    assert "JSONRenderer" in renderer_types
    assert "HumanReadableRenderer" not in renderer_types

    # Test testing mode - should use HumanReadableRenderer
    configure_structlog(testing=True)
    config = structlog.get_config()

    renderer_types = [type(processor).__name__ for processor in config["processors"]]
    assert "HumanReadableRenderer" in renderer_types
    assert "JSONRenderer" not in renderer_types
