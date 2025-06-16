import logging
import os
import sys
from datetime import datetime

class LogGen:
    @staticmethod
    def loggen():
        logger = logging.getLogger("automationLogger")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Timestamped log filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = f"automation_{timestamp}.log"

            # Logs directory
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logs_dir = os.path.join(base_dir, "Logs")
            os.makedirs(logs_dir, exist_ok=True)

            log_path = os.path.join(logs_dir, log_filename)
            print(f"📁 Logging to: {log_path}")

            # File handler
            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))

            # Attach handlers
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger
