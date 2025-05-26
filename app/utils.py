from app.dao.dao import Main_menuDao, TableDao, TimeslotDao
from app.dao.database import async_session_maker

menu = [{'name' : 'main', 'description' : "👋 Добро пожаловать в Binary Bites! 🍽️\n\nЗдесь каждый байт вкуса закодирован в удовольствие. 😋💻\n"
            "Используйте клавиатуру ниже, чтобы зарезервировать свой столик и избежать переполнения буфера! 🔢🍴"},
        {'name': 'about',
         'description': "🖥️ О Binary Bites 🍔\n\n"
        "Мы - первый ресторан, где кулинария встречается с кодом! 👨‍💻👩‍💻\n\n"
        "🍽️ Наше меню - это настоящий алгоритм вкуса:\n\n"
        "• Закуски начинаются с 'Hello World' салата 🥗\n"
        "• Основные блюда включают 'Full Stack' бургер 🍔\n"
        "• Не забудьте про наш фирменный 'Python' кофе ☕\n\n"
        "🏆 Наша миссия - оптимизировать ваше гастрономическое удовольствие!\n\n"
        "📍 Мы находимся по адресу: ул. Программная, д. 404\n"
        "🕒 Работаем 24/7, потому что настоящие разработчики не спят😉\n\n"
        "Приходите к нам, чтобы отладить свой аппетит! 🍽️💻"}
        ]
table = [{ "id": 1, "capacity": 1, "description": "Уютный столик для двоих у окна" },
         { "id": 2, "capacity": 1, "description": "Уютный столик для двоих у окна" },
         { "id": 3, "capacity": 2, "description": "Уютный столик для двоих у окна" },
         { "id": 4, "capacity": 2, "description": "Уютный столик для двоих у окна" },
         { "id": 5, "capacity": 3, "description": "Уютный столик для двоих у окна" },]

time = [{ "id": 1, "start_time": "06:00", "stop_time": "08:00" },
        { "id": 2, "start_time": "08:00", "stop_time": "10:00" },
        { "id": 3, "start_time": "10:00", "stop_time": "12:00" },
        { "id": 4, "start_time": "12:00", "stop_time": "14:00" },
        { "id": 5, "start_time": "14:00", "stop_time": "16:00" },
        { "id": 6, "start_time": "16:00", "stop_time": "18:00" },
        { "id": 7, "start_time": "18:00", "stop_time": "20:00" },
        { "id": 8, "start_time": "20:00", "stop_time": "22:00" },
        ]


async def add_db():
    async with async_session_maker() as session:
        await Main_menuDao(session).add_all(menu)
        await TableDao(session).add_all(table)
        await TimeslotDao(session).add_all(time)
