import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("flask").setLevel(logging.WARNING)


current_date = datetime.now().strftime("%Y-%m-%d")
file_handler = logging.FileHandler(f"logs/scrooge_{current_date}.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)




def get_logger(name):
    logger = logging.getLogger(name)
    
    logger.setLevel(logging.INFO)

    logger.propagate = False

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


groq_logger = get_logger("groq")
app_logger = get_logger("app")
bot_logger = get_logger("bot")