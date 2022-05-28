from distutils import log
import logging
import sys

__version__ = 3.0
__author__ = "Adam Walkiewicz"
github = "https://github.com/ajwalkiewicz/sound-pad"

DEFAULT_LOGGING_LEVEL = logging.ERROR

LOGGING_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def main():
    if len(sys.argv) > 1:
        logging_level = LOGGING_LEVEL_MAP.get(str(sys.argv[1]).lower(), "error")
    else:
        logging_level = DEFAULT_LOGGING_LEVEL

    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
        level=logging_level,
    )
    print(f"Logging level set to: {logging_level}")

    import modules.app as app
    app.run()


if __name__ == "__main__":
    main()
