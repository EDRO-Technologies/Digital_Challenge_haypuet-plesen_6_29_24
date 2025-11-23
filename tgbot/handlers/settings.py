from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.api_client import APIClient

SELECT_GROUP = range(1)


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать настройки уведомлений"""
    user_id = update.message.from_user.id
    
    # Получаем текущие настройки пользователя
    user_settings = APIClient.get_user_settings(user_id)
    current_status = user_settings.get('notifications_enabled', True)
    
    group_text = APIClient.get_user_group(user_id)['name']
    if not group_text:
        group_text = 'Не установлена'
    
    status_text = "🔔 Включены" if current_status else "🔕 Выключены"
    
    keyboard_buttons = []
    if not current_status:
        keyboard_buttons.append([InlineKeyboardButton("🔔 Включить уведомления", callback_data="notifications_on")])
    else:
        keyboard_buttons.append([InlineKeyboardButton("🔕 Выключить уведомления", callback_data="notifications_off")])
    
    keyboard_buttons.append([InlineKeyboardButton("👥 Задать номер группы", callback_data="group_settings")])
    
    keyboard_buttons.append([InlineKeyboardButton("◀️ Назад в главное меню", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    await update.message.reply_text(
        f"⚙️ Настройки:\n\n"
        f"Уведомления: {status_text}\n\n"
        f"🎓 Группа: {group_text}\n\n"
        f"Выберите действие:",
        reply_markup=keyboard
    )

async def handle_notification_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка переключения уведомлений"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    
    # Определяем новое значение настроек
    if action == "notifications_on":
        notifications_enabled = True
        success_message = "✅ Уведомления включены! Вы будете получать уведомления о новых мероприятиях."
    elif action == "notifications_off":
        notifications_enabled = False
        success_message = "🔕 Уведомления выключены! Вы не будете получать уведомления о новых мероприятиях."
    elif action == "setgroup":
        notifications_enabled = False
        success_message = "🔕 Уведомления выключены! Вы не будете получать уведомления о новых мероприятиях."
    elif action == "back_to_main":
        await show_main_menu(query)
        return
    
    # Сохраняем настройки в API/БД
    success = APIClient.update_user_settings(user_id, notifications_enabled)
    
    if success:
        # Логируем действие
        print(f"📝 User {user_id} ({user_name}) changed notifications to: {notifications_enabled}")
        
        # Обновляем сообщение с новыми настройками
        status_text = "🔔 Включены" if notifications_enabled else "🔕 Выключены"
        
        keyboard_buttons = []
        if not notifications_enabled:
            keyboard_buttons.append([InlineKeyboardButton("🔔 Включить уведомления", callback_data="notifications_on")])
        else:
            keyboard_buttons.append([InlineKeyboardButton("🔕 Выключить уведомления", callback_data="notifications_off")])
        
        keyboard_buttons.append([InlineKeyboardButton("◀️ Назад в главное меню", callback_data="back_to_main")])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        await query.edit_message_text(
            f"⚙️ Настройки уведомлений:\n\n"
            f"Текущий статус: {status_text}\n\n"
            f"{success_message}",
            reply_markup=keyboard
        )
    else:
        await query.edit_message_text(
            "❌ Произошла ошибка при сохранении настроек. Попробуйте позже."
        )

async def show_main_menu(query):
    """Показать главное меню"""
    keyboard = [
        ['📅 Мое расписание', '🎉 Мероприятия'],
        ['⚙️ Настройки']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Редактируем существующее сообщение или отправляем новое
    try:
        await query.edit_message_text(
            'Главное меню:',
            reply_markup=None  # Убираем inline-клавиатуру
        )
    except:
        pass  # Если не можем редактировать, продолжаем
    
    # await query.message.reply_text('Главное меню:', reply_markup=reply_markup)

def get_user_notifications_status(user_id: int) -> bool:
    """Получить статус уведомлений пользователя (для использования в других модулях)"""
    user_settings = APIClient.get_user_settings(user_id)
    return user_settings.get('notifications_enabled', True)