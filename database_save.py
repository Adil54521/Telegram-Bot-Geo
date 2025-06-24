import sqlite3
from datetime import datetime

# Инициализация базы данных: создание таблицы visits, если она ещё не существует
def init_db():
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный id для ключа и команда AUTOINCREMENT для автоматического увеличения значения при каждом обновлении статуса
            telegram_id INTEGER NOT NULL,         -- Айди телеграма и обязательная команда INTEGER NOT NULL для недопущения ошибки пустого поля
            username TEXT,                        -- Имя пользователя 
            action_type TEXT NOT NULL,            -- "пришел" или "ушел"
            date TEXT NOT NULL,                   -- Дата 
            time TEXT NOT NULL,                   -- Время посещения в формате HH:MM:SS
            address TEXT,                         -- Адрес, полученный по координатам
            latitude REAL,                        -- Широта 
            longitude REAL                        -- Долгота
        )
    """)
    conn.commit()
    conn.close()

# Сохраняет информацию о посещении в базу данных
def save_visit(telegram_id, username, action_type, address=None, latitude=None, longitude=None):
    now = datetime.now() # Инициализация функции из datetime
    date = now.strftime("%Y-%m-%d") # определение переменной для хранения данных по дате 
    time = now.strftime("%H:%M:%S") # определение переменной для хранения данных по времени 
    conn = sqlite3.connect("visits.db") # создаёт соединение с БД visits.db (файл будет создан, если его ещё нет) 
    cursor = conn.cursor() # Инициализация объекта cursor()  
    cursor.execute("""
        INSERT INTO visits (telegram_id, username, action_type, date, time, address, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (telegram_id, username, action_type, date, time, address, latitude, longitude)) # выполняет SQL-запрос
    conn.commit()
    conn.close()
    
# Собирает данные для команды статистика 
# Получает список посещений пользователя за сегодняшний день
def get_today_visits(telegram_id):
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action_type, time, address
        FROM visits
        WHERE telegram_id = ? AND date = ?
        ORDER BY time ASC
    """, (telegram_id, today))
   
    results = cursor.fetchall()
    # Получаем все строки результата в виде списка кортежей
    conn.close()
    return results
