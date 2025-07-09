import logging
import os
import sys

import colorlog

from src import config


def _initLogger(level: str = "info"):
    match level.lower():
        case "debug":
            level = logging.DEBUG
        case "info":
            level = logging.INFO
        case "warning":
            level = logging.WARNING
        case "error":
            level = logging.ERROR
        case "fatal":
            level = logging.FATAL
        case _:
            level = logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    handler = colorlog.StreamHandler()

    # 定义日志格式，其中可以指定各个等级的颜色
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] - [%(levelname)s] - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    formatterNoColor = colorlog.ColoredFormatter(
        '[%(asctime)s] - [%(levelname)s] - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # 设置处理器的格式
    handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(handler)

    if not os.path.exists(os.path.dirname(config.DEBUG_FILE_PATH)):
        os.makedirs(os.path.dirname(config.DEBUG_FILE_PATH))
        open(config.DEBUG_FILE_PATH, "w").close()

    fileHandle = logging.FileHandler(config.DEBUG_FILE_PATH, mode="w", encoding="utf-8")
    fileHandle.setLevel(level)
    fileHandle.setFormatter(formatterNoColor)

    logger.addHandler(fileHandle)
    return logger


__logger = _initLogger(config.LOGGER_LEVEL)


def debug(msg: str, *args, **kwargs):
    __logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs):
    __logger.info(msg, *args, **kwargs)


def warn(msg: str, *args, **kwargs):
    __logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs):
    __logger.error(msg, *args, **kwargs)


def fatal(msg: str, *args, **kwargs):
    __logger.fatal(msg, *args, **kwargs)
    sys.exit(1)


if __name__ == '__main__':
    # initLogger("debug")
    __logger.debug("测试s")
    __logger.info("测试s")
    __logger.warning("测试s")
    __logger.error("测试s")
    __logger.fatal("测试s")
