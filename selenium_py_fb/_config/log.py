from logging.config import dictConfig


def init_logger():
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "selenium_py_fb.simple": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                "style": "%",
            },
        },
        "handlers": {
            "selenium_py_fb.console": {
                "class": "logging.StreamHandler",
                "formatter": "selenium_py_fb.simple",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "selenium_py_fb": {
                "handlers": ["selenium_py_fb.console"],
                "propagate": False,
                "level": "DEBUG",
            },
        },
    }
    dictConfig(LOGGING)
