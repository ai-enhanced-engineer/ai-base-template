"""Functional tests for the logger module."""

import json
from typing import Any

import pytest
from pytest import LogCaptureFixture, MonkeyPatch

from src.logging import (
    bind_context_vars,
    clear_context_fields,
    configure_structlog,
    get_correlation_id,
    get_logger,
)

# Test Helpers


def parse_log_json(caplog: LogCaptureFixture, index: int = 0) -> dict[str, Any]:
    """Parse log record as JSON with helpful error context."""
    try:
        return json.loads(caplog.records[index].message)
    except (json.JSONDecodeError, IndexError) as e:
        records = [r.message for r in caplog.records]
        raise AssertionError(f"Failed to parse log {index}: {e}. Records: {records}")


def assert_json_log_structure(log_data: dict[str, Any]) -> None:
    """Verify log has required JSON structure."""
    required_fields = {"timestamp", "level", "logger", "message", "context"}
    missing_fields = required_fields - log_data.keys()
    assert not missing_fields, f"Missing required fields: {missing_fields}"


def assert_human_readable_format(log_message: str) -> None:
    """Verify log is human-readable format (not JSON)."""
    with pytest.raises((json.JSONDecodeError, ValueError)):
        json.loads(log_message)

    # Should contain basic readable components
    assert "[" in log_message and "]" in log_message
    assert ":" in log_message


@pytest.fixture(autouse=True)
def setup_logger():
    configure_structlog()
    yield
    clear_context_fields()


# Correlation ID Tests


@pytest.mark.parametrize(
    "correlation_id",
    [
        "simple-123",
        "very-long-correlation-id-with-lots-of-characters-12345",
        "req-abc-123",
    ],
)
def test_correlation_id_appears_in_logs(caplog: LogCaptureFixture, correlation_id: str):
    bind_context_vars(correlation_id=correlation_id)

    get_logger("test").info("Test message")

    log_data = parse_log_json(caplog)
    assert log_data["extra"]["correlation_id"] == correlation_id


def test_correlation_id_defaults_to_unknown():
    clear_context_fields()
    assert get_correlation_id() == "unknown"


def test_correlation_id_propagates_across_loggers(caplog: LogCaptureFixture):
    bind_context_vars(correlation_id="propagate-test")

    get_logger("auth").info("Auth step")
    get_logger("db").info("DB step")
    get_logger("api").info("Response step")

    for i in range(3):
        log_data = parse_log_json(caplog, i)
        assert log_data["extra"]["correlation_id"] == "propagate-test"


def test_context_isolation_between_requests(caplog: LogCaptureFixture):
    # First request
    bind_context_vars(correlation_id="req-1", user_id="user-1")
    get_logger("handler").info("First request")

    # Clear context (simulates end of request)
    clear_context_fields()

    # Second request
    bind_context_vars(correlation_id="req-2")  # Note: no user_id
    get_logger("handler").info("Second request")

    first_log = parse_log_json(caplog, 0)
    second_log = parse_log_json(caplog, 1)

    assert first_log["extra"]["correlation_id"] == "req-1"
    assert first_log["extra"]["user_id"] == "user-1"

    assert second_log["extra"]["correlation_id"] == "req-2"
    assert "user_id" not in second_log.get("extra", {})


# Log Output Format Tests


def test_json_output_structure(caplog: LogCaptureFixture):
    get_logger("test").info("Test message", custom_field="custom_value")

    log_data = parse_log_json(caplog)
    assert_json_log_structure(log_data)

    assert log_data["message"] == "Test message"
    assert log_data["logger"] == "test"
    assert log_data["level"] == "info"
    assert log_data["extra"]["custom_field"] == "custom_value"


def test_custom_fields_go_to_extra(caplog: LogCaptureFixture):
    get_logger("api").info("API call", user_id="user-123", endpoint="/api/chat", status_code=200)

    log_data = parse_log_json(caplog)

    # Standard fields at root
    assert_json_log_structure(log_data)

    # Custom fields in extra
    extra = log_data["extra"]
    assert extra["user_id"] == "user-123"
    assert extra["endpoint"] == "/api/chat"
    assert extra["status_code"] == 200

    # Standard fields not in extra
    standard_fields = {"timestamp", "level", "message", "logger", "context"}
    assert not (standard_fields & extra.keys())


@pytest.mark.parametrize(
    "testing,should_be_json",
    [
        (False, True),  # Production mode = JSON
        (True, False),  # Testing mode = Human readable
    ],
)
def test_output_format_based_on_testing_flag(caplog: LogCaptureFixture, testing: bool, should_be_json: bool):
    configure_structlog(testing=testing)
    bind_context_vars(correlation_id="format-test")

    get_logger("format").info("Format test", field="value")

    log_message = caplog.records[0].message

    if should_be_json:
        log_data = parse_log_json(caplog)
        assert_json_log_structure(log_data)
        assert log_data["extra"]["correlation_id"] == "format-test"
    else:
        assert_human_readable_format(log_message)
        assert "Format test" in log_message
        assert "field=value" in log_message
        assert "[id:format-t]" in log_message  # Truncated correlation ID


# Human-Readable Formatter Tests


def test_human_readable_complete_log_formatting(caplog: LogCaptureFixture):
    configure_structlog(testing=True)
    bind_context_vars(correlation_id="complete-test-789")

    get_logger("services.llm").warning("LLM call completed", duration_ms=2500, model="gpt-4o-mini")

    output = caplog.records[0].message

    # Verify format components
    assert "[WARNING]" in output
    assert "services.llm:" in output
    assert "LLM call completed" in output
    assert "duration_ms=2500" in output
    assert "model=gpt-4o-mini" in output
    assert "[id:complete]" in output  # Truncated to 8 chars

    # Verify timestamp format (HH:MM:SS at start)
    import re

    assert re.match(r"^\d{2}:\d{2}:\d{2}", output)


def test_human_readable_handles_missing_fields_gracefully(caplog: LogCaptureFixture):
    configure_structlog(testing=True)
    get_logger("simple").error("Simple error")

    output = caplog.records[0].message

    assert "[ERROR]" in output
    assert "simple:" in output
    assert "Simple error" in output

    # Should not have correlation ID or extra brackets
    assert "[id:" not in output
    assert "[]" not in output


def test_human_readable_logger_name_abbreviation(caplog: LogCaptureFixture):
    configure_structlog(testing=True)

    test_cases = [
        ("src.core.chat", "core.chat"),
        ("src.api.threads", "api.threads"),
        ("src.main", "main"),
        ("external.logger", "external.logger"),  # Non-src loggers unchanged
    ]

    for full_name, expected_abbrev in test_cases:
        get_logger(full_name).info("Test")
        output = caplog.records[-1].message
        assert f"{expected_abbrev}:" in output


@pytest.mark.parametrize(
    "correlation_id,expected_display",
    [
        ("short", "[id:short]"),
        ("very-long-correlation-id-123456789", "[id:very-lon]"),
        ("", ""),  # Empty correlation ID should not display
    ],
)
def test_human_readable_correlation_id_truncation(
    caplog: LogCaptureFixture, correlation_id: str, expected_display: str
):
    configure_structlog(testing=True)

    if correlation_id:
        bind_context_vars(correlation_id=correlation_id)
    else:
        clear_context_fields()

    get_logger("test").info("Correlation test")

    output = caplog.records[0].message
    if expected_display:
        assert expected_display in output
    else:
        assert "[id:" not in output


# Configuration Tests


def test_log_level_filtering(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.setenv("LOGGING_LEVEL", "WARNING")
    configure_structlog()

    logger = get_logger("test")
    logger.debug("Should not appear")
    logger.info("Should not appear")
    logger.warning("Should appear")
    logger.error("Should appear")

    messages = [parse_log_json(caplog, i)["message"] for i in range(len(caplog.records))]

    assert "Should not appear" not in " ".join(messages)
    assert "Should appear" in " ".join(messages)
    assert len(caplog.records) == 2  # Only WARNING and ERROR


def test_invalid_log_level_defaults_to_info(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.setenv("LOGGING_LEVEL", "INVALID")
    configure_structlog()

    logger = get_logger("test")
    logger.debug("Debug message")
    logger.info("Info message")

    # Should default to INFO level, so debug filtered out
    assert len(caplog.records) == 1
    log_data = parse_log_json(caplog)
    assert log_data["message"] == "Info message"


# Edge Cases


def test_extremely_long_field_values(caplog: LogCaptureFixture):
    configure_structlog(testing=True)

    very_long_value = "x" * 100
    get_logger("test").info("Long value test", long_field=very_long_value)

    output = caplog.records[0].message

    # Should be truncated with "..."
    assert "long_field=" in output
    assert "..." in output
    assert very_long_value not in output  # Full value should not appear


def test_empty_or_none_values(caplog: LogCaptureFixture):
    get_logger("test").info("Empty test", empty_string="", none_value=None, zero_value=0, false_value=False)

    log_data = parse_log_json(caplog)
    extra = log_data["extra"]

    assert extra["empty_string"] == ""
    assert extra["none_value"] is None
    assert extra["zero_value"] == 0
    assert extra["false_value"] is False


def test_special_characters_in_fields(caplog: LogCaptureFixture):
    special_chars = 'Test with "quotes", commas, and [brackets]'
    get_logger("test").info("Special chars", special_field=special_chars)

    log_data = parse_log_json(caplog)
    assert log_data["extra"]["special_field"] == special_chars
