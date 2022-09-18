from loguru import logger

# logger.add('info.log', format='{time} {level} {message}', level="INFO", rotation="500 MB", compression='zip')
logger.add('error.log', format='{time} {level} {message}', level="ERROR", rotation="500 MB" , compression='zip')
logger.add('debug.log', format='{time} {level} {message}', level="DEBUG", rotation="500 MB" , compression='zip')