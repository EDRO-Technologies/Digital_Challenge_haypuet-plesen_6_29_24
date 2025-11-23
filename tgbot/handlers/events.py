from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from services.api_client import APIClient
from handlers.settings import get_user_notifications_status
import re
from datetime import datetime

# Состояния для ConversationHandler
EVENT_TITLE, EVENT_DATE, EVENT_TIME, EVENT_DURATION = range(4)

async def show_events_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать меню мероприятий"""
    keyboard = [
        ['📋 Все мероприятия', '✅ Мои мероприятия'],
        ['📝 Создать мероприятие', '◀️ Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('🎉 Меню мероприятий:', reply_markup=reply_markup)

async def show_all_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать все мероприятия с информацией о конфликтах"""
    try:
        user_id = update.message.from_user.id
        events = _get_mock_events()
        
        if not events:
            await update.message.reply_text('📭 На данный момент нет активных мероприятий.')
            return

        events_text = "🎉 Все активные мероприятия:\n\n"
        
        for i, event in enumerate(events, 1):
            events_text += f"**{i}. {event['title']}**\n"
            # events_text += f"📅 {event['date']} в {event['time']} ({_format_duration(event['duration'])})\n"
            events_text += f"📅 {datetime.fromisoformat(event['date']).strftime('%d.%m.%Y')} в {datetime.fromisoformat(event['date']).strftime('%H:%M')} ({_format_duration(event['duration'])})\n"
            # events_text += f"📝 {event['description']}\n"
            events_text += f"👤 Создатель: {event['created_by_user']['name']}\n"
            events_text += f"👥 Участников: {event['participants_count']}\n"
            
            # Проверяем участие
            is_participating = _is_user_participating(user_id, event['id'])
            if is_participating:
                events_text += "✅ Вы участвуете\n"
            else:
                # Проверяем конфликт времени с учетом продолжительности
                conflict_check = APIClient.check_time_conflict(
                    user_id, datetime.fromisoformat(event['date']).strftime("%d.%m.%Y"), datetime.fromisoformat(event['date']).strftime("%H:%M"),event['duration']
                )
                if conflict_check['has_conflict']:
                    events_text += "⚠️ **Конфликт времени!**\n"
                    # Добавляем информацию о конфликтующих событиях
                    for conflict in conflict_check['conflicting_events']:
                        events_text += f"   └─ 🚫 Конфликтует с: {conflict['title']} ({conflict['time']}, {_format_duration(conflict['duration'])})\n"
                else:
                    events_text += "❌ Вы не участвуете\n"
            
            events_text += f"🎯 ID: {event['id']}\n\n"

        # Добавляем кнопки для участия для ВСЕХ мероприятий (включая конфликтующие)
        keyboard = []
        for event in events:
            if not _is_user_participating(user_id, event['id']):
                # Проверяем конфликт с учетом продолжительности
                conflict_check = APIClient.check_time_conflict(
                    user_id, datetime.fromisoformat(event['date']).strftime("%d.%m.%Y"), datetime.fromisoformat(event['date']).strftime("%H:%M"),event['duration']
                )
                
                if conflict_check['has_conflict']:
                    # Для конфликтующих событий показываем специальную кнопку с предупреждением
                    button_text = f"⚠️ Участвовать (ЕСТЬ КОНФЛИКТ) - '{event['title'][:15]}...'"
                else:
                    button_text = f"✅ Участвовать в '{event['title'][:15]}...'"
                
                keyboard.append([InlineKeyboardButton(
                    button_text, 
                    callback_data=f"participate_{event['id']}"
                )])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        if len(events_text) > 4000:
            parts = [events_text[i:i+4000] for i in range(0, len(events_text), 4000)]
            for part in parts[:-1]:
                await update.message.reply_text(part)
            await update.message.reply_text(parts[-1], reply_markup=reply_markup)
        else:
            await update.message.reply_text(events_text, reply_markup=reply_markup)

    except Exception as e:
        print(f"Error showing events: {e}")
        await update.message.reply_text('❌ Ошибка при загрузке мероприятий')

async def show_my_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать мероприятия, в которых участвует пользователь"""
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.full_name
        
        # ЗАГЛУШКА: получение мероприятий пользователя
        my_events = _get_mock_my_events(user_id)
        
        if not my_events:
            await update.message.reply_text(
                '📭 Вы пока не участвуете ни в одном мероприятии.\n\n'
                'Нажмите "📋 Все мероприятия" чтобы посмотреть доступные события!'
            )
            return

        events_text = f"✅ Ваши мероприятия, {user_name}:\n\n"
        
        for i, event in enumerate(my_events, 1):
            events_text += f"**{i}. {event['title']}**\n"
            events_text += f"📅 {event['date']} в {event['time']} ({_format_duration(event['duration'])})\n"
            # events_text += f"📝 {event['description']}\n"
            events_text += f"👤 Создатель: {event['created_by_user']['name']}\n"
            events_text += f"👥 Всего участников: {event['participants_count']}\n"
            events_text += f"🎯 ID: {event['id']}\n\n"

        # Кнопка для просмотра всех мероприятий
        keyboard = [
            [InlineKeyboardButton("📋 Посмотреть все мероприятия", callback_data="show_all_events")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(events_text, reply_markup=reply_markup)

    except Exception as e:
        print(f"Error showing my events: {e}")
        await update.message.reply_text('❌ Ошибка при загрузке ваших мероприятий')

def _get_mock_events():
    """получение тестовых мероприятий с продолжительностью"""
    
    return APIClient.get_all_events()
    
    return [
        {
            'id': 'event_001',
            'title': 'Встреча IT-клуба',
            'description': 'Обсуждение новых технологий и проектов',
            'date': '15.12.2024',
            'time': '18:00',
            'duration': 120,  # 2 часа в минутах
            'creator_name': 'Алексей Петров',
            'participants_count': 8,
            'participants': [397924277, 1896651602]
        },
        {
            'id': 'event_002', 
            'title': 'Мастер-класс по Python',
            'description': 'Практическое занятие для начинающих',
            'date': '17.12.2024',
            'time': '16:30',
            'duration': 90,  # 1.5 часа в минутах
            'creator_name': 'Мария Сидорова',
            'participants_count': 12,
            'participants': [397924277]
        },
        {
            'id': 'event_003',
            'title': 'Хакатон 2024',
            'description': 'Главное IT-событие года',
            'date': '20.12.2024', 
            'time': '10:00',
            'duration': 480,  # 8 часов в минутах
            'creator_name': 'Иван Иванов',
            'participants_count': 25,
            'participants': []
        },
        {
            'id': 'event_004',
            'title': 'Совещание по проекту',
            'description': 'Планирование следующего спринта',
            'date': '17.12.2024',
            'time': '17:00',  # Начинается через 30 минут после мастер-класса
            'duration': 60,   # 1 час в минутах
            'creator_name': 'Петр Сергеев',
            'participants_count': 5,
            'participants': []
        }
    ]

def _format_duration(duration_minutes: int) -> str:
    """Форматирует продолжительность в читаемый вид"""
    if duration_minutes < 60:
        return f"{duration_minutes} мин"
    else:
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        if minutes == 0:
            return f"{hours} ч"
        else:
            return f"{hours} ч {minutes} мин"

def _get_mock_my_events(user_tgid):
    all_events = _get_mock_events()
    my_events = []
    user_id = APIClient.user_by_tgid(user_tgid)
    
    for event in all_events:
        if user_id in event['participants']:
            my_events.append(event)
    print(my_events)
    return my_events

def _is_user_participating(user_tgid, event_id):
    """Проверяет, участвует ли пользователь в мероприятии"""
    events = _get_mock_events()
    user_id = APIClient.user_by_tgid(user_tgid)
    for event in events:
        print("event['id'] == event_id", event['id'], event_id, event['id'] == event_id)
        if event['id'] == event_id:
            print(user_id)
            return user_id in event['participants']
    return False

def _get_event_by_id(event_id):
    """Получить мероприятие по ID"""
    events = _get_mock_events()
    for event in events:
        if int(event['id']) == int(event_id):
            return event
    return None

async def start_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания мероприятия"""
    await update.message.reply_text(
        "📝 Создание нового мероприятия\n\nВведите название мероприятия:"
    )
    return EVENT_TITLE

async def handle_event_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка названия мероприятия"""
    context.user_data['event_title'] = update.message.text
    await update.message.reply_text("Введите дату мероприятия (в формате ДД.ММ.ГГГГ):")
    return EVENT_DATE

# async def handle_event_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработка описания мероприятия"""
#     context.user_data['event_description'] = update.message.text
#     await update.message.reply_text("Введите дату мероприятия (в формате ДД.ММ.ГГГГ):")
#     return EVENT_DATE

async def handle_event_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка даты мероприятия"""
    date_text = update.message.text
    if not re.match(r'\d{2}\.\d{2}\.\d{4}', date_text):
        await update.message.reply_text("❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ:")
        return EVENT_DATE
    
    context.user_data['event_date'] = date_text
    await update.message.reply_text("Введите время мероприятия (в формате ЧЧ:ММ):")
    return EVENT_TIME

async def handle_event_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка времени мероприятия"""
    time_text = update.message.text
    if not re.match(r'\d{2}:\d{2}', time_text):
        await update.message.reply_text("❌ Неверный формат времени. Используйте ЧЧ:ММ:")
        return EVENT_TIME
    
    context.user_data['event_time'] = time_text
    await update.message.reply_text(
        "Введите продолжительность мероприятия в минутах:\n\n"
        "Примеры:\n"
        "• 30 - 30 минут\n"
        "• 60 - 1 час\n" 
        "• 90 - 1.5 часа\n"
        "• 120 - 2 часа"
    )
    return EVENT_DURATION
    
async def handle_event_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка продолжительности мероприятия и финальное создание"""
    try:
        duration_text = update.message.text
        duration = int(duration_text)
        
        if duration <= 0:
            await update.message.reply_text("❌ Продолжительность должна быть положительным числом. Попробуйте еще раз:")
            return EVENT_DURATION
        
    except ValueError:
        await update.message.reply_text("❌ Неверный формат. Введите число (минуты):")
        return EVENT_DURATION
    
    # Сбор данных мероприятия
    event_data = {
        'title': context.user_data['event_title'],
        # 'description': context.user_data['event_description'],
        'date': str(datetime.strptime(f"{context.user_data['event_date']} {context.user_data['event_time']}", "%d.%m.%Y %H:%M")),
        # 'time': context.user_data['event_time'],
        'duration': duration,
        'created_by': update.message.from_user.id,
        'creator_name': update.message.from_user.full_name
    }
    
    # Отправка в API
    result = APIClient.create_event(event_data)
    
    if result:
        event_id = result.get('id', 'unknown')
        await update.message.reply_text(
            f"✅ Мероприятие '{event_data['title']}' успешно создано!\n"
            f"⏱ Продолжительность: {_format_duration(duration)}\n"
            f"Уведомления отправлены пользователям."
        )
        
        # Отправка уведомлений другим пользователям
        await _notify_users_about_event(context.bot, event_data, event_id)
    else:
        await update.message.reply_text("❌ Ошибка при создании мероприятия")
    
    # Очистка временных данных
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена создания мероприятия"""
    context.user_data.clear()
    await update.message.reply_text("Создание мероприятия отменено.")
    return ConversationHandler.END

async def _notify_users_about_event(bot, event_data: dict, event_id: str):
    """Отправка уведомлений о новом мероприятии пользователям с включенными уведомлениями"""
    # ЗАГЛУШКА: получаем пользователей
    users = _get_users_with_enabled_notifications()
    
    notified_count = 0
    for user in users:
        try:
            
            # Проверяем, что у пользователя включены уведомления
            if get_user_notifications_status(user['telegram_id']):
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Участвовать", callback_data=f"participate_{event_id}")
                ]])
                print("h222ello")
                
                message_text = (
                    f"🎉 Новое мероприятие!\n\n"
                    f"📌 {event_data['title']}\n"
                    f"📅 {str(event_data['date'])}\n"
                    # f"📅 {datetime.strftime(str(event_data['date']), '%d.%m.%Y')} в {datetime.strftime(str(event_data['time']), '%H:%M')}\n"
                    # f"📝 {event_data['description']}\n"
                    f"👤 Создатель: {event_data['creator_name']}"
                )
                
                print("333")
                await bot.send_message(
                    chat_id=user['telegram_id'],
                    text=message_text,
                    reply_markup=keyboard
                )
                notified_count += 1
                
        except Exception as e:
            print(f"Error sending notification to user {user['telegram_id']}: {e}")
    
    print(f"📢 Notifications sent: {notified_count} users notified about event {event_id}")

def _get_users_with_enabled_notifications():
    """получение пользователей с включенными уведомлениями"""
    # В реальном приложении здесь будет вызов APIClient.get_users_with_notifications()
    # return [
    #     {'user_id': 397924277, 'username': 'test_user_1'},
    #     {'user_id': 1896651602, 'username': 'test_user_2'}
    # ]
    return APIClient.get_users_with_notifications()

async def handle_participation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки участия с проверкой конфликта времени"""
    query = update.callback_query
    await query.answer()
    
    event_id = query.data.replace('participate_', '')
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    
    # Получаем информацию о мероприятии
    event_info = _get_event_by_id(event_id)
    if not event_info:
        await query.edit_message_text(
            text=query.message.text + "\n\n❌ Мероприятие не найдено.",
            reply_markup=None
        )
        return
    
    # Проверяем конфликт времени с учетом продолжительности
    conflict_check = APIClient.check_time_conflict(
        user_id, 
        event_info['date'], 
        event_info['time'],
        event_info['duration']
    )
    
    if conflict_check['has_conflict']:
        # Показываем предупреждение о конфликте
        await _show_time_conflict_warning(query, event_info, conflict_check['conflicting_events'])
        return
    
    # Если конфликта нет, продолжаем запись
    user_data = {
        'id': user_id,
        'user_name': user_name,
        'username': query.from_user.username
    }
    
    success = APIClient.participate_event(event_id, user_data)
    
    if success:
        # Обновляем сообщение
        new_text = query.message.text + f"\n\n✅ {user_name} записан(а) на мероприятие!"
        await query.edit_message_text(
            text=new_text,
            reply_markup=None
        )
        
        # Отправляем подтверждение в личку
        await query.message.reply_text(
            f"🎉 Вы успешно записались на мероприятие!\n\n"
            f"📌 *{event_info['title']}*\n"
            f"📅 {event_info['date']} в {event_info['time']}\n"
            f"⏱ Продолжительность: {_format_duration(event_info['duration'])}\n\n"
            f"Не забудьте добавить его в свой календарь 📅"
        )
    else:
        await query.edit_message_text(
            text=query.message.text + "\n\n❌ Ошибка записи. Попробуйте позже.",
            reply_markup=None
        )

async def _show_time_conflict_warning(query, event_info, conflicting_events):
    """Показать предупреждение о конфликте времени с информацией о продолжительности"""
    conflict_text = (
        f"⚠️ **Обнаружен конфликт времени!**\n\n"
        f"Вы уже участвуете в другом мероприятии в это же время:\n\n"
    )
    
    for conflict in conflicting_events:
        conflict_text += (
            f"📌 **{conflict['title']}**\n"
            f"📅 {conflict['date']} в {conflict['time']} ({_format_duration(conflict['duration'])})\n"
            # f"📝 {conflict['description']}\n\n"
        )
    
    conflict_text += (
        f"❌ Вы не можете участвовать в мероприятии:\n"
        f"**{event_info['title']}**\n"
        f"📅 {event_info['date']} в {event_info['time']} ({_format_duration(event_info['duration'])})\n\n"
        f"Пожалуйста, выберите другое время или отмените участие в конфликтующем мероприятии."
    )
    
    # Создаем клавиатуру с опциями
    keyboard = [
        [InlineKeyboardButton("📋 Мои мероприятия", callback_data="show_my_events_from_conflict")],
        [InlineKeyboardButton("📅 Все мероприятия", callback_data="show_all_events_from_conflict")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_participation")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=conflict_text,
        reply_markup=reply_markup
    )

async def handle_conflict_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка действий при конфликте времени"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "show_my_events_from_conflict":
        await show_my_events_from_conflict(query, context)
    elif action == "show_all_events_from_conflict":
        await show_all_events_from_conflict(query, context)
    elif action == "cancel_participation":
        await cancel_participation_conflict(query, context)

async def show_my_events_from_conflict(query, context):
    """Показать мероприятия пользователя из конфликтной ситуации"""
    try:
        user_id = query.from_user.id
        my_events = _get_mock_my_events(user_id)
        
        if not my_events:
            await query.edit_message_text(
                '📭 Вы пока не участвуете ни в одном мероприятии.'
            )
            return

        events_text = "✅ Ваши мероприятия:\n\n"
        
        for i, event in enumerate(my_events, 1):
            events_text += f"**{i}. {event['title']}**\n"
            events_text += f"📅 {event['date']} в {event['time']}\n"
            # events_text += f"📝 {event['description']}\n"
            events_text += f"🎯 ID: {event['id']}\n\n"

        # Кнопки для навигации
        keyboard = [
            [InlineKeyboardButton("📋 Все мероприятия", callback_data="show_all_events")],
            [InlineKeyboardButton("◀️ Назад в главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(events_text, reply_markup=reply_markup)

    except Exception as e:
        print(f"Error showing my events from conflict: {e}")
        await query.edit_message_text('❌ Ошибка при загрузке ваших мероприятий')

async def show_all_events_from_conflict(query, context):
    """Показать все мероприятия из конфликтной ситуации"""
    # Создаем фейковый update объект для вызова существующей функции
    class FakeUpdate:
        def __init__(self, query):
            self.callback_query = query
    
    fake_update = FakeUpdate(query)
    await handle_show_all_events_callback(fake_update, context)

async def cancel_participation_conflict(query, context):
    """Отмена участия при конфликте"""
    await query.edit_message_text(
        "❌ Запись на мероприятие отменена из-за конфликта времени.\n\n"
        "Вы можете выбрать другое мероприятие или изменить время участия в существующих."
    )

async def handle_show_all_events_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка callback для показа всех мероприятий"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "show_all_events":
        await show_all_events_from_callback(query, context)

async def show_all_events_from_callback(query, context):
    """Показать все мероприятия из callback"""
    try:
        user_id = query.from_user.id
        events = _get_mock_events()
        
        if not events:
            await query.edit_message_text('📭 На данный момент нет активных мероприятий.')
            return

        events_text = "🎉 Все активные мероприятия:\n\n"
        for i, event in enumerate(events, 1):
            events_text += f"*{i}. {event['name']}*\n"
            events_text += f"📅 {event['date'].strftime('%d.%m.%Y')} в {datetime.fromisoformat(event['date']).strftime('%H:%M')}\n"
            # events_text += f"📝 {event['description']}\n"
            events_text += f"👤 Создатель: {event['creator_name']}\n"
            events_text += f"👥 Участников: {event['participants_count']}\n"
            
            is_participating = _is_user_participating(user_id, event['id'])
            if is_participating:
                events_text += "✅ Вы участвуете\n"
            else:
                conflict_check = APIClient.check_time_conflict(user_id, datetime.fromisoformat(event['date']).strftime("%d.%m.%Y"), datetime.fromisoformat(event['date']).strftime("%H:%M"),event['duration'])
                if conflict_check['has_conflict']:
                    events_text += "⚠️ **Конфликт времени!**\n"
                else:
                    events_text += "❌ Вы не участвуете\n"
            
            events_text += f"🎯 ID: {event['id']}\n\n"

        keyboard = []
        for event in events:
            if not _is_user_participating(user_id, event['id']):
                conflict_check = APIClient.check_time_conflict(user_id, datetime.fromisoformat(event['date']).strftime("%d.%m.%Y"), datetime.fromisoformat(event['date']).strftime("%H:%M"),event['duration'])
                if not conflict_check['has_conflict']:
                    keyboard.append([InlineKeyboardButton(
                        f"✅ Участвовать в '{event['title'][:20]}...'", 
                        callback_data=f"participate_{event['id']}"
                    )])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await query.edit_message_text(events_text, reply_markup=reply_markup)

    except Exception as e:
        print(f"Error showing events from callback: {e}")
        await query.edit_message_text('❌ Ошибка при загрузке мероприятий')