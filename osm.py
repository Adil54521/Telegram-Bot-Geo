import asyncio # Для работы с асинхронными функциями и задачами
import aiohttp # Для выполнения асинхронных HTTP-запросов (например, к API геолокации)
from datetime import datetime # Для получения текущей даты и времени
import logging # Для вывода логов (отладочной информации)
from aiogram import Router, F # Импорт роутера и фильтров из Aiogram для обработки сообщений
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton # Типы сообщений и кнопки клавиатуры
from database_save import init_db, save_visit # Импорт функций для работы с базой данных
from keyboards import main_menu_keyboard # Импорт главного меню (reply-клавиатура)

# Создаём экземпляр роутера, в котором будут зарегистрированы все обработчики из этого файла
router = Router() # Инициализация метода Router()
user_action_map = {} # Словарь куда будут собираться данные по статусам пришел, ушел

logging.basicConfig( # Включаем логирование: показывает время, тип сообщения и текст
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

async def reverse_geocode(lat, lon):
    # URL сервис Nominatim для обратного геокодирования (получение адреса по координатам)
    url = "https://nominatim.openstreetmap.org/reverse"
    # Параметры запроса: координаты и формат ответа (JSON)
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1
    }
    # Запрос в по url адресу с указанием "паспортных данных"
    headers = {
        "User-Agent": "BotForGeolocation/1.0 (@GeoAdresBot)"
    }
    # 
    async with aiohttp.ClientSession() as session:
        # Отправляем GET-запрос с координатами и заголовками
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                # Если запрос успешен — получаем JSON-ответ
                data = await response.json()
                address = data.get("address", {})
                # Извлекаем нужные поля из адреса (если есть)
                result = {
                    "display_name": data.get("display_name"),
                    "country": address.get("country"),
                    "city": address.get("city") or address.get("town") or address.get("village"),
                    "road": address.get("road"),
                    "house_number": address.get("house_number")
                }
                return result
            else:
                # None если ошибка
                return None

async def location_reply_button():
    # Создаётся клавиатура с одной кнопкой — "Отправить местоположение"
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить местоположение", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return location_keyboard

@router.message(F.location) # Обработчик срабатывает, если пользователь отправил геолокацию
async def handle_location(message: Message):
    from_user_id = message.from_user.id  # Получаем Telegram ID пользователя и передаем в переменную
    action = user_action_map.get(from_user_id, "пришел") # Получаем действие из словаря (пришел/ушел), по умолчанию — "пришел"
    
    # Извлекаются координаты полученные в reverse_geocode
    lat = message.location.latitude
    lon = message.location.longitude
    logging.info(f"Получено местоположение: {lat}, {lon}")
    
    # Получаем адрес по координатам с помощью API Nominatim
    address = await reverse_geocode(lat, lon)
    
    # Получаем текущую дату и время
    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M")
    
    # Если адрес успешно получен
    if address:
        address_str = address['display_name'] # Полный адрес
        init_db() # Создаём таблицу, если ещё не создана
        # Сохраняем посещение в базу данных
        save_visit(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            action_type=action,
            address=address_str,
            latitude=lat,
            longitude=lon
        )
         # Отправляем пользователю подтверждение
        await message.answer(
            f"{action.capitalize()} зафиксирован:\n"
            f"Дата: {date}\n"
            f"Время: {time_str}\n"
            f"Местоположение: {address_str}"
        )
        logging.info(f"{action.capitalize()} сохранён в БД.")
         # Возвращаем пользователя в главное меню
        await message.answer("Возврат к главному меню:", reply_markup=main_menu_keyboard())
    else:
         # Если не удалось получить адрес по координатам
        await message.answer("Не удалось определить адрес по координатам.")
        logging.warning("Адрес не определён.")
