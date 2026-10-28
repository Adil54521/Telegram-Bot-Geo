📍 Telegram Attendance Bot
A Telegram bot for tracking user actions (arrived / left) and saving them to a database.

All data is stored in a local SQLite database (visits.db) and includes:
- 🆔 Telegram ID
- 👤 Username (if available)
- 🕹 Action type: arrived or left
- 🗓 Date and 🕒 time
- 📍 Address determined from coordinates (via Nominatim / OpenStreetMap)
- 🌐 Geographic coordinates (latitude and longitude)
- 
✨ Features
- 📦 Stores attendance records in SQLite
- 📍 Button for sharing the user’s location
- 🌐 Determines the exact address based on coordinates
- ⚙️ Supports asynchronous operation using aiogram
- 📅 Automatically records the current date and time
- 
🛠 Technologies
- Python 3.9+
- aiogram
- sqlite3 (built into Python)
- aiohttp — for sending requests to Nominatim
- dotenv — for loading environment variables (bot token)
