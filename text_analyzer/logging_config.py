import logging
import structlog


def setup_logging() -> None:
  """
  Настраивает структурированное логирование через structlog.
  Логи выводятся в формате JSON.
  """
  structlog.configure(
    processors=[
      structlog.stdlib.add_log_level,
      structlog.processors.TimeStamper(fmt='iso'),
      structlog.processors.StackInfoRenderer(),
      structlog.processors.format_exc_info,
      structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
  )

  logging.basicConfig(
    format='%(message)s',
    level=logging.INFO,
  )