import logging
import os
import sys
from typing import Any

import structlog
from structlog.types import EventDict, WrappedLogger

LOG_SPECIFIC_FIELDS = {
    "timestamp",
    "logger",
    "message",
    "context",
    "level",
}


def _process_log_fields(logger: WrappedLogger, log_method: str, event_dict: EventDict) -> EventDict:
    # Rename "event" to "message"
    event_dict["message"] = event_dict.pop("event", "")
    event_dict["context"] = structlog.contextvars.get_contextvars().get("context", "default")

    # Create the "extra" dictionary for unexpected keys
    extra_fields = {key: event_dict.pop(key) for key in list(event_dict.keys()) if key not in LOG_SPECIFIC_FIELDS}

    # Add the "extra" dictionary if it contains any fields
    if extra_fields:
        event_dict["extra"] = extra_fields

    return event_dict


def _abbreviate_logger_name(logger_name: str) -> str:
    """Abbreviate logger names for readable output."""
    if not logger_name.startswith("src"):
        return logger_name

    # Remove the src prefix and return the meaningful part
    parts = logger_name.replace("src.", "").split(".")

    # Keep last 2 parts for context (e.g., "core.chat", "services.llm")
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"
    return parts[-1] if parts else logger_name


def _format_extra_fields(extra: dict[str, Any]) -> str:
    """Format extra fields for human-readable output."""
    if not extra:
        return ""

    # Prioritize important fields
    important_keys = ["status_code", "duration_ms", "response_size_bytes", "error", "sql_query"]
    formatted_parts = []

    # Add important fields first
    for key in important_keys:
        if key in extra:
            value = extra[key]
            if key == "duration_ms":
                formatted_parts.append(f"{value}ms")
            elif key == "status_code":
                formatted_parts.append(f"HTTP {value}")
            elif key == "response_size_bytes":
                formatted_parts.append(f"{value}B")
            else:
                formatted_parts.append(f"{key}={value}")

    # Add remaining fields
    remaining = {k: v for k, v in extra.items() if k not in important_keys}
    for key, value in remaining.items():
        if len(str(value)) > 50:  # Truncate long values
            formatted_parts.append(f"{key}={str(value)[:47]}...")
        else:
            formatted_parts.append(f"{key}={value}")

    return f" [{', '.join(formatted_parts)}]" if formatted_parts else ""


class HumanReadableRenderer:
    """Human-readable log formatter for testing environments."""

    def __call__(self, logger: WrappedLogger, log_method: str, event_dict: EventDict) -> str:
        """Render log entry in human-readable format: HH:MM:SS [LEVEL] logger: message [key_info] [correlation_id]"""
        # Extract components
        timestamp = event_dict.get("timestamp", "")
        level = event_dict.get("level", "").upper()
        logger_name = _abbreviate_logger_name(event_dict.get("logger", ""))
        message = event_dict.get("message", "")
        extra = event_dict.get("extra", {})
        correlation_id = structlog.contextvars.get_contextvars().get("correlation_id", "")

        # Format timestamp to HH:MM:SS
        time_part = ""
        if timestamp:
            try:
                # Extract time from ISO timestamp (e.g., "2025-01-27T14:30:45.123456")
                if "T" in timestamp:
                    time_part = timestamp.split("T")[1].split(".")[0]  # Get HH:MM:SS part
                else:
                    time_part = timestamp.split(" ")[1].split(".")[0] if " " in timestamp else timestamp
            except (IndexError, AttributeError):
                time_part = timestamp

        # Build the formatted message
        parts = []
        if time_part:
            parts.append(time_part)
        if level:
            parts.append(f"[{level}]")
        if logger_name:
            parts.append(f"{logger_name}:")
        if message:
            parts.append(message)

        base_message = " ".join(parts)

        # Add extra fields if present
        extra_str = _format_extra_fields(extra)
        if extra_str:
            base_message += extra_str

        # Add correlation ID if present
        if correlation_id:
            base_message += f" [id:{correlation_id[:8]}]"

        return base_message


def configure_structlog(testing: bool = False) -> None:
    """Configure structured logging with JSON or human-readable output format."""
    # Get logging level from environment or default to INFO
    log_level = os.environ.get("LOGGING_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(format="%(message)s", level=level, stream=sys.stdout)
    logging.getLogger().setLevel(level)

    # Silence LiteLLM's verbose logging - let our app control what gets logged
    litellm_logger = logging.getLogger("LiteLLM")
    litellm_log_level = os.environ.get("LITELLM_LOG_LEVEL", "WARNING").upper()
    litellm_level = getattr(logging, litellm_log_level, logging.WARNING)
    litellm_logger.setLevel(litellm_level)

    # Common processors
    base_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        _process_log_fields,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # Add renderer based on testing flag
    renderer = HumanReadableRenderer() if testing else structlog.processors.JSONRenderer()
    processors = base_processors + [renderer]

    structlog.configure(
        processors=processors,  # type: ignore[arg-type]
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )


# Direct assignments for context management
clear_context_fields = structlog.contextvars.clear_contextvars
bind_contextvars = structlog.contextvars.bind_contextvars
get_contextvars = structlog.contextvars.get_contextvars


def get_correlation_id() -> str:
    """Get correlation ID from context or return default."""
    contextvars = structlog.contextvars.get_contextvars()
    return str(contextvars.get("correlation_id", "unknown"))


def get_logger(name: str = "") -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name or __name__)  # type: ignore
