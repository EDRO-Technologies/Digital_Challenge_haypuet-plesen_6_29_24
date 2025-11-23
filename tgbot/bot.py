from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
import config
from services.api_client import APIClient

# Импорт обработчиков
from handlers.schedule import handle_schedule_request, show_schedule_periods
from handlers.events import (
    start_event_creation, handle_event_title,
    handle_event_date, handle_event_time, handle_event_duration, cancel_event_creation, handle_participation,
    show_events_menu, show_all_events, show_my_events, handle_show_all_events_callback,
    handle_conflict_resolution,
    EVENT_TITLE, EVENT_DATE, EVENT_TIME, EVENT_DURATION
)
from handlers.settings import show_settings, handle_notification_toggle

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    APIClient.user_database_check(update.message.from_user)
    """Главное меню"""
    keyboard = [
        ['📅 Мое расписание', '🎉 Мероприятия'],
        ['📝 Создать мероприятие', '⚙️ Настройки']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Главное меню:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    
    if text == '📅 Мое расписание':
        await show_schedule_periods(update, context)
    elif text == '🎉 Мероприятия':
        await show_events_menu(update, context)
    elif text in ['📅 Сегодня', '📅 Завтра', '📅 Понедельник', '📅 Вторник', 
                  '📅 Среда', '📅 Четверг', '📅 Пятница', '📅 Суббота',
                  '📅 На неделю', '◀️ Назад']:
        await handle_schedule_request(update, context)
    elif text in ['📋 Все мероприятия', '✅ Мои мероприятия', '📝 Создать мероприятие']:
        await handle_events_actions(update, context)
    elif text == '⚙️ Настройки':
        await show_settings(update, context)
    else:
        await update.message.reply_text('Используйте кнопки меню для навигации')

async def handle_events_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик действий с мероприятиями"""
    text = update.message.text
    
    if text == '📋 Все мероприятия':
        await show_all_events(update, context)
    elif text == '✅ Мои мероприятия':
        await show_my_events(update, context)
    elif text == '📝 Создать мероприятие':
        await start_event_creation(update, context)
    elif text == '◀️ Назад':
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    keyboard = [
        ['📅 Мое расписание', '🎉 Мероприятия'],
        ['⚙️ Настройки']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Если это callback query (из настроек)
    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.message.reply_text('Главное меню:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Главное меню:', reply_markup=reply_markup)

def setup_handlers(application):
    """Настройка всех обработчиков"""
    
    # ConversationHandler для создания мероприятий
    event_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^📝 Создать мероприятие$'), start_event_creation)],
        states={
            EVENT_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_event_title)],
            # EVENT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_event_description)],
            EVENT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_event_date)],
            EVENT_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_event_time)],
            EVENT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_event_duration)],
        },
        fallbacks=[CommandHandler('cancel', cancel_event_creation)]
    )
    
    # Основные обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(event_conv_handler)
    application.add_handler(CallbackQueryHandler(handle_participation, pattern="^participate_"))
    application.add_handler(CallbackQueryHandler(handle_conflict_resolution, pattern="^(show_my_events_from_conflict|show_all_events_from_conflict|cancel_participation)$"))
    application.add_handler(CallbackQueryHandler(handle_show_all_events_callback, pattern="^show_all_events$"))
    application.add_handler(CallbackQueryHandler(handle_notification_toggle, pattern="^(notifications_on|notifications_off|back_to_main)$"))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

def main():
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    setup_handlers(application)
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()