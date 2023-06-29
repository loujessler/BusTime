import logging
from loguru import logger

from data import config


# Level       Numeric value
# CRITICAL         50
# ERROR            40
# WARNING          30
# INFO             20
# DEBUG            10
# NOTSET            0

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


class LoguruLogger:
    def __init__(self):
        # Удаляем все предыдущие обработчики
        logger.remove()
        # Добавляем новый уровень логирования с именем "USER", номером 25 (что между INFO и WARNING) и иконкой
        logger.level("USER", no=25, icon="👤", color="<yellow>")

    # Функции-фильтры для каждого уровня логирования
    @staticmethod
    def user_only(record):
        return record["level"].no == 25

    @staticmethod
    def debug_only(record):
        return record["level"].no == 10  # DEBUG level number is 10

    @staticmethod
    def info_only(record):
        return record["level"].no == 20  # INFO level number is 20

    @staticmethod
    def warning_only(record):
        return record["level"].no == 30  # WARNING level number is 30

    @staticmethod
    def error_only(record):
        return record["level"].no == 40  # ERROR level number is 40

    @staticmethod
    def critical_only(record):
        return record["level"].no == 50  # CRITICAL level number is 50

    def setup_loguru(self):
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level.name}</level> | <level>{message}</level>"

        # Максимальный размер каждого файла лога: 5 МБ
        max_log_size = "5 MB"

        # Добавляем обработчики для каждого уровня логирования
        logger.add("logs/user.log",
                   filter=self.user_only,
                   format=log_format,
                   rotation="5 MB",
                   compression="zip",
                   colorize=True)
        logger.add("logs/info.log",
                   filter=self.info_only,
                   format=log_format,
                   colorize=True,
                   rotation=max_log_size,
                   compression="zip")
        logger.add("logs/warning.log",
                   filter=self.warning_only,
                   format=log_format,
                   colorize=True,
                   rotation=max_log_size,
                   compression="zip")
        logger.add("logs/error.log",
                   filter=self.error_only,
                   format=log_format,
                   colorize=True,
                   rotation=max_log_size,
                   compression="zip")
        logger.add("logs/critical.log",
                   filter=self.critical_only,
                   format=log_format,
                   colorize=True,
                   rotation=max_log_size,
                   compression="zip")
        if not config.SERVER_MODE:
            logger.add("logs/debug.log",
                       filter=self.debug_only,
                       format=log_format,
                       colorize=True,
                       rotation=max_log_size,
                       compression="zip")
            logger.add("logs.log",
                       format=log_format,
                       level=config.DEBUG,
                       rotation=max_log_size,
                       compression="zip",
                       colorize=True)
