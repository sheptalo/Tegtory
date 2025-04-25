import logging
from typing import Any

COLORS = {
    "DEBUG": "\033[94m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[95m",
}


class CustomFormatter(logging.Formatter):
    info = "\033[92m"
    debug = "\033[94m"
    warning = "\033[93m"
    error = "\x1b[31;20m"
    crit = "\x1b[31;1m"
    reset = "\x1b[0m"

    message_format = (
        "%(asctime)s | %(levelname)-7s | %(name)-50s | "
        f"%(message)-100s {reset} | %(filename)s:%(lineno)d"
    )

    FORMATS = {
        logging.DEBUG: debug + message_format,
        logging.INFO: info + message_format,
        logging.WARNING: warning + message_format,
        logging.ERROR: error + message_format,
        logging.CRITICAL: crit + message_format,
    }

    def format(self, record: logging.LogRecord) -> Any:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%d-%m-%Y %H:%M")
        return formatter.format(record)


class LoggerClass(logging.Logger):
    def __init__(self, record: logging.Logger) -> None:
        logging.Logger.__init__(record, logging.DEBUG)


def configure_logger() -> None:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logging.basicConfig(level=logging.DEBUG, handlers=[ch])
