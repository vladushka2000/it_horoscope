import copy


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
            }
        },
    "root": {
        "level": "INFO",
        "handlers": [],
        "propagate": True
    },
}


def get_dev_config() -> dict:
    logger_config = copy.deepcopy(LOGGING)
    logger_config["root"]["handlers"].extend(["default"])
    logger_config["root"]["level"] = "DEBUG"

    return logger_config


def get_prod_config() -> dict:
    logger_config = copy.deepcopy(LOGGING)
    logger_config["root"]["handlers"].extend(["default"])

    return logger_config
