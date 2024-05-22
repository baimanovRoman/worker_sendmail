import logging
import inspect

from settings import LOG_AVAILABLE_LEVELS


def logger(level: str="ERROR", message: str=None):
    """Запись в логи происходит c фиксацией модуля, c которого вызвана функция"""

    assert message, "Не указан message"
    level = level.upper()
    assert level in LOG_AVAILABLE_LEVELS, f"Допустимые значения level: {LOG_AVAILABLE_LEVELS}, введён {level}"

    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    logger = logging.getLogger(mod.__name__)

    return logger.log(getattr(logging, level), message)