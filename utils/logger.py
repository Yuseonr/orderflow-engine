import logging
import os

def setLogger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Creates or retrieves a customized logger that writes to a specific file.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

ENGINE_LOGGER = setLogger('EngineLogger', 'logs/engine.log')
SIGNAL_LOGGER = setLogger('SignalLogger', 'logs/signal.log')
