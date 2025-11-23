from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from services.api_client import APIClient
import requests
import config

async def show_schedule_periods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать выбор периода для расписания"""
    keyboard = [
        ['📅 Сегодня', '📅 Завтра'],
        ['📅 Понедельник', '📅 Вторник', '📅 Среда'],
        ['📅 Четверг', '📅 Пятница', '📅 Суббота'],
        ['📅 На неделю', '◀️ Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите период для просмотра расписания:', reply_markup=reply_markup)

async def handle_schedule_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик запросов расписания для разных периодов"""
    text = update.message.text
    
    if text == '📅 Сегодня':
        await get_schedule_for_date(update, context, datetime.now())
    elif text == '📅 Завтра':
        await get_schedule_for_date(update, context, datetime.now() + timedelta(days=1))
    elif text == '📅 Понедельник':
        await get_schedule_for_weekday(update, context, 0)  # 0 = Monday
    elif text == '📅 Вторник':
        await get_schedule_for_weekday(update, context, 1)  # 1 = Tuesday
    elif text == '📅 Среда':
        await get_schedule_for_weekday(update, context, 2)  # 2 = Wednesday
    elif text == '📅 Четверг':
        await get_schedule_for_weekday(update, context, 3)  # 3 = Thursday
    elif text == '📅 Пятница':
        await get_schedule_for_weekday(update, context, 4)  # 4 = Friday
    elif text == '📅 Суббота':
        await get_schedule_for_weekday(update, context, 5)  # 5 = Saturday
    elif text == '📅 На неделю':
        await get_weekly_schedule(update, context)
    elif text == '◀️ Назад':
        await show_main_menu(update, context)

async def get_schedule_for_date(update: Update, context: ContextTypes.DEFAULT_TYPE, date_obj):
    """Получить расписание на конкретную дату"""
    try:
        date_str = date_obj.strftime('%Y-%m-%d')
        day_name = get_russian_day_name(date_obj.weekday())
        formatted_date = date_obj.strftime('%d.%m.%Y')
        
        # ЗАГЛУШКА вместо реального API
        schedule = _get_mock_schedule_for_date(date_obj,update.message.from_user.id)
        
        if not schedule:
            await update.message.reply_text(
                f"📅 {day_name}, {formatted_date}\n\n"
                f"Занятий нет! 🎉"
            )
            return

        lessons_text = f"📅 {day_name}, {formatted_date}\n\n"
        for lesson in schedule:
            lessons_text += f"🕒 {lesson['time']}\n"
            lessons_text += f"📚 {lesson['subject']}\n"
            lessons_text += f"👨‍🏫 {lesson['teacher']}\n"
            lessons_text += f"🏫 {lesson['room']}\n\n"

        await update.message.reply_text(lessons_text)

    except Exception as e:
        await update.message.reply_text('❌ Ошибка при получении расписания')

async def get_schedule_for_weekday(update: Update, context: ContextTypes.DEFAULT_TYPE, weekday):
    """Получить расписание на конкретный день недели"""
    try:
        today = datetime.now()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:  # Если день уже прошел на этой неделе
            days_ahead += 7
        target_date = today + timedelta(days=days_ahead)
        
        await get_schedule_for_date(update, context, target_date)
        
    except Exception as e:
        await update.message.reply_text('❌ Ошибка при получении расписания')

async def get_weekly_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить расписание на всю неделю"""
    try:
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weekly_text = "📅 Расписание на неделю\n\n"
        
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_name = get_russian_day_name(i)
            formatted_date = day_date.strftime('%d.%m.%Y')
            
            # ЗАГЛУШКА: получаем расписание для дня
            schedule = _get_mock_schedule_for_date(day_date,update.message.from_user.id)
            weekly_text += f"{day_name}, {formatted_date}\n"
            
            if not schedule:
                
                weekly_text += "   Занятий нет\n\n"
            else:
                print(schedule)
                
                for lesson in schedule[:2]:  # Показываем только первые 2 занятия для краткости
                # for lesson in schedule:  # Показываем только первые 2 занятия для краткости
                    weekly_text += f"   🕒 {lesson['time']} - {lesson['subject']}\n"
                if len(schedule) > 2:
                    weekly_text += f"   ... и ещё {len(schedule) - 2} занятий\n"
                weekly_text += "\n"
        
        # Если текст слишком длинный, разбиваем на части
        if len(weekly_text) > 4000:
            parts = [weekly_text[i:i+4000] for i in range(0, len(weekly_text), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(weekly_text)
            
    except Exception as e:
        print(f"Error showing events: {e}")
        await update.message.reply_text('❌ Ошибка при получении недельного расписания')

def _get_mock_schedule_for_date(date_obj, user_tgid):
    """ЗАГЛУШКА: получение тестового расписания для даты"""
    weekday = date_obj.weekday()
    group_id = APIClient.get_user_group(user_tgid)
    shed_data = APIClient.get_events_by_group(group_id)
    print(shed_data)
    
    shed_formated = convert_schedule(shed_data)
    print(shed_formated)
    return shed_formated.get(weekday, [])
    
    # Разное расписание для разных дней недели
    # schedules = {
    #     0: [  # Понедельник
    #         {'time': '09:00-10:30', 'subject': 'Математика', 'teacher': 'Иванов И.И.', 'room': '101'},
    #         {'time': '11:00-12:30', 'subject': 'Физика', 'teacher': 'Петров П.П.', 'room': '203'},
    #         {'time': '14:00-15:30', 'subject': 'Информатика', 'teacher': 'Сидорова А.В.', 'room': 'Компьютерный класс'}
    #     ],
    #     1: [  # Вторник
    #         {'time': '10:00-11:30', 'subject': 'Химия', 'teacher': 'Кузнецова М.В.', 'room': '305'},
    #         {'time': '12:00-13:30', 'subject': 'Биология', 'teacher': 'Орлова С.Н.', 'room': '412'}
    #     ],
    #     2: [  # Среда
    #         {'time': '09:00-10:30', 'subject': 'История', 'teacher': 'Николаев Д.С.', 'room': '215'},
    #         {'time': '11:00-12:30', 'subject': 'Литература', 'teacher': 'Фёдорова Е.П.', 'room': '118'}
    #     ],
    #     3: [  # Четверг
    #         {'time': '13:00-14:30', 'subject': 'Английский язык', 'teacher': 'Smith J.', 'room': '201'},
    #         {'time': '15:00-16:30', 'subject': 'Физкультура', 'teacher': 'Котов В.Г.', 'room': 'Спортзал'}
    #     ],
    #     4: [  # Пятница
    #         {'time': '10:00-11:30', 'subject': 'География', 'teacher': 'Павлов А.М.', 'room': '307'},
    #         {'time': '12:00-13:30', 'subject': 'Экономика', 'teacher': 'Зайцева Т.К.', 'room': '404'}
    #     ],
    #     5: [],  # Суббота - нет занятий
    #     6: []   # Воскресенье - нет занятий
        
    # }
    # wff = {0: [{'time': '08:30-09:50', 'subject': 'Вычислительная математика (лек)', 'teacher': 'Дубовик А.О.', 'room': 'А613'},
    #          {'time': '08:30-09:50', 'subject': 'Дискретная математика (лек)', 'teacher': 'Мухутдинова Д.Р.', 'room': 'А613'}, 
    #          {'time': '09:50-11:10', 'subject': 'Дискретная математика (пр)', 'teacher': 'Мухутдинова Д.Р.', 'room': 'А613'}, 
    #          {'time': '11:10-12:30', 'subject': 'Статистические методы и модели управления', 'teacher': 'Курамшина А.В.', 'room': 'У606'}, 
    #          {'time': '11:10-12:30', 'subject': 'Технология программиров.', 'teacher': 'Берестин Д.К.', 'room': 'У607'}
    #          ], 
    #      1: [{'time': '08:30-09:50', 'subject': 'Русский язык и культура речи (пр)', 'teacher': 'Хадынская А.А.', 'room': 'А539'}, 
    #          {'time': '09:50-11:10', 'subject': 'Вычислительная математика (пр)', 'teacher': 'Дубовик А.О.', 'room': 'У506'}, 
    #          {'time': '11:10-12:30', 'subject': 'Иностранный язык', 'teacher': 'Грамма Д.В.', 'room': 'У507'}, 
    #          {'time': '11:10-12:30', 'subject': 'Статистические методы и модели управления', 'teacher': 'Курамшина А.В.', 'room': 'У802'}, {'time': '12:30-13:50', 'subject': 'Технология программирования', 'teacher': 'Берестин Д.К.', 'room': 'У606'}, {'time': '12:30-13:50', 'subject': 'Мультимедиа технологии', 'teacher': 'Кучин И.А.', 'room': 'У706'}], 2: [{'time': '09:50-11:10', 'subject': 'Информ. технологии', 'teacher': 'Берестин Д.К.', 'room': 'У607'}, {'time': '11:10-12:30', 'subject': 'Иностранный язык', 'teacher': 'Пичуева А.В.', 'room': 'У508'}, {'time': '12:30-13:50', 'subject': 'Мультимедиа технологии (лек)', 'teacher': 'Кучин И.А.', 'room': 'У902'}, {'time': '13:50-15:10', 'subject': 'Мультимедиа технологии', 'teacher': 'Кучин И.А.', 'room': 'У706'}], 3: [{'time': '08:30-09:50', 'subject': 'Статистические методы и модели управления (лек)', 'teacher': 'Курамшина А.В.', 'room': 'К613'}, {'time': '09:50-11:10', 'subject': 'Основы экономической культуры (пр)', 'teacher': 'Минникова Ю.М.', 'room': 'К613'}], 4: [{'time': '12:30-13:50', 'subject': 'Информационные технологии (лек)', 'teacher': 'Берестин Д.К.', 'room': 'У708'}, {'time': '12:30-13:50', 'subject': 'Технология программирования (лек)', 'teacher': 'Берестин Д.К.', 'room': 'У708'}, {'time': '13:50-15:10', 'subject': 'Информ. технологии', 'teacher': 'Берестин Д.К.', 'room': 'У607'}], 5: [{'time': '11:10-12:30', 'subject': 'Основы WEB-инжиниринга (лек)', 'teacher': 'Кучин И.А.', 'room': 'У708'}, {'time': '12:30-13:50', 'subject': 'Основы WEB-инжиниринга', 'teacher': 'Кучин И.А.', 'room': 'У706'}, {'time': '12:30-13:50', 'subject': 'Основы WEB-инжиниринга', 'teacher': 'Кучин И.А.', 'room': 'У706'}], 6: []}
    
    # return wff.get(weekday, [])

def convert_schedule(original_data):
    schedules = {i: [] for i in range(7)}  # 0-6 для понедельника-воскресенья
    
    for lesson in original_data:
        # Преобразуем день недели (1-7 -> 0-6)
        day = lesson['week_day'] - 1
        
        # Преобразуем timestamp в форматированное время
        start_time = datetime.fromtimestamp(lesson['time'])
        end_time = start_time + timedelta(minutes=lesson['duration'])
        time_str = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
        
        # Формируем запись занятия
        schedule_entry = {
            'time': time_str,
            'subject': lesson['name'],
            'teacher': lesson['teacher_user']['name'],
            'room': lesson['location_instance']['room']
        }
        
        schedules[day].append(schedule_entry)
    
    # Сортируем занятия по времени для каждого дня
    for day in schedules:
        schedules[day].sort(key=lambda x: x['time'])
    
    return schedules

def get_russian_day_name(weekday):
    """Получить русское название дня недели"""
    days = {
        0: "Понедельник",
        1: "Вторник", 
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    return days.get(weekday, "Неизвестный день")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    from bot import show_main_menu as main_menu
    await main_menu(update, context)