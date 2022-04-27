import logging
import sys

__version__ = 3.0
__author__ = "Adam Walkiewicz"
github = "https://github.com/ajwalkiewicz/sound-pad"

LOGGING_LEVEL = logging.INFO
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
    level=LOGGING_LEVEL
    )

system = sys.platform
if system == "linux":
    logging.info(f"System detected: {system}")
    import modules.linux_app as app
    app.run()
elif system == "win32":
    logging.info(f"System detected: {system}")
    import modules.win_app as app
    app.run()
else:
    logging.info(f"System detected: {system}, runing in linux configuration")
    import modules.linux_app as app
    app.run()
