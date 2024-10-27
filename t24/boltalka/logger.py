import logging
import time

# Создаем объект логгера
logger = logging.getLogger()

# Устанавливаем уровень логирования
logger.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
handler = logging.StreamHandler()

# Форматируем сообщения с временем
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)