from loguru import logger

logger.add(
    "dead_letters.log",
    rotation="10 MB",
    retention=5,
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[reason]} | {extra[exchange]} | {extra[queue]} | {extra[routing_key]} | {extra[body]}",
    level="INFO"
)