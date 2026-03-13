from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Основная клавиатура"""
    keyboard = [
        ['🔍 Найти проект', '📋 Мои проекты'],
        ['👤 Мой профиль', '💡 Создать проект'],
        ['🎯 Рекомендации', '❓ Помощь']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_cancel_keyboard():
    """Клавиатура с кнопкой отмены"""
    keyboard = [['❌ Отмена']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_project_actions_keyboard(project_id: int, is_creator: bool = False):
    """Клавиатура действий с проектом"""
    keyboard = []
    
    if is_creator:
        keyboard.append([InlineKeyboardButton("📋 Заявки", callback_data=f"applications_{project_id}")])
        keyboard.append([InlineKeyboardButton("✏️ Редактировать", callback_data=f"edit_{project_id}")])
        keyboard.append([InlineKeyboardButton("❌ Закрыть проект", callback_data=f"close_{project_id}")])
    else:
        keyboard.append([InlineKeyboardButton("📝 Подать заявку", callback_data=f"apply_{project_id}")])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_projects")])
    
    return InlineKeyboardMarkup(keyboard)

def get_categories_keyboard():
    """Клавиатура категорий проектов"""
    categories = [
        'Веб-разработка', 'Мобильные приложения', 'Дизайн', 
        'Маркетинг', 'Наука/Data Science', 'Игры', 
        'Искусственный интеллект', 'Другое'
    ]
    
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(category, callback_data=f"cat_{category}")])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)