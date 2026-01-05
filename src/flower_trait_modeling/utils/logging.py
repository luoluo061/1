"""Logging utilities for the flower trait modeling system.

This module centralizes logging configuration to ensure each sub-package
produces structured and consistent log messages. The helpers here are small
and intentionally dependency-light so they can be reused in scripts, tests,
and application code without pulling heavy frameworks.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LogConfig:
    """Configuration for loggers used across the project.

    Attributes:
        level: The log level name such as ``"INFO"``.
        fmt: The log message format.
        datefmt: The date format string.
        stream: Optional stream target, defaults to ``sys.stdout``.
    """

    level: str = "INFO"
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    stream: Any = sys.stdout

    def to_kwargs(self) -> Dict[str, Any]:
        """Convert configuration to a dictionary for ``logging.basicConfig``."""

        return {
            "level": getattr(logging, self.level.upper(), logging.INFO),
            "format": self.fmt,
            "datefmt": self.datefmt,
            "stream": self.stream,
        }


_DEFAULT_CONFIG = LogConfig()


def configure_logging(config: Optional[LogConfig] = None) -> logging.Logger:
    """Configure root logging using the provided configuration.

    This function is idempotent; subsequent calls will not reconfigure the root
    logger if handlers are already present.

    Args:
        config: Optional custom :class:`LogConfig`.

    Returns:
        A logger configured with the provided settings.
    """

    cfg = config or _DEFAULT_CONFIG
    if logging.getLogger().handlers:
        return logging.getLogger("flower_trait_modeling")

    logging.basicConfig(**cfg.to_kwargs())
    logger = logging.getLogger("flower_trait_modeling")
    logger.debug("Logging configured", extra={"config": cfg})
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a child logger using the module name.

    Args:
        name: Logical module path to append to the root logger name.

    Returns:
        A :class:`logging.Logger` instance ready for use.
    """

    configure_logging()
    return logging.getLogger(f"flower_trait_modeling.{name}")


__all__ = ["LogConfig", "configure_logging", "get_logger"]
