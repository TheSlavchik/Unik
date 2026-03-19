import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ConversationHandler, filters,
    ContextTypes
)
from config import BOT_TOKEN
from database import Database
from keyboards import (
    get_main_keyboard, get_cancel_keyboard, 
    get_project_actions_keyboard, get_categories_keyboard
)
5
# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
(PROFILE_ROLE, PROFILE_SKILLS, PROFILE_INTERESTS, PROFILE_ABOUT,
 PROJECT_TITLE, PROJECT_DESCRIPTION, PROJECT_CATEGORY, PROJECT_SKILLS,
 APPLY_MESSAGE) = range(9)

# Инициализация базы данных
db = Database()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Сохраняем пользователя в БД
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я помогу тебе найти проекты по интересам и команду для реализации идей.\n\n"
        "Что я умею:\n"
        "🔍 Искать проекты по категориям и навыкам\n"
        "📋 Показывать твои проекты и заявки\n"
        "👤 Создавать профиль с твоими навыками\n"
        "💡 Помогать создавать новые проекты\n"
        "🎯 Давать рекомендации на основе твоих навыков\n\n"
        "Давай начнем! Для начала заполни свой профиль."
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )
    
    # Предлагаем заполнить профиль
    await update.message.reply_text(
        "Хочешь заполнить профиль сейчас? Это поможет находить более релевантные проекты.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Заполнить профиль", callback_data="fill_profile"),
            InlineKeyboardButton("⏰ Позже", callback_data="later")
        ]])
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "📚 **Справка по командам:**\n\n"
        "🔍 **Найти проект** - поиск проектов по категориям\n"
        "📋 **Мои проекты** - проекты, где вы участвуете или создали\n"
        "👤 **Мой профиль** - просмотр и редактирование профиля\n"
        "💡 **Создать проект** - создание нового проекта\n"
        "🎯 **Рекомендации** - проекты, подходящие под ваши навыки\n"
        "❓ **Помощь** - показать это сообщение\n\n"
        "Для поиска проектов используйте кнопки меню или команды:\n"
        "/start - начать работу\n"
        "/profile - мой профиль\n"
        "/projects - список проектов\n"
        "/create - создать проект"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Обработчики текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == '🔍 Найти проект':
        await find_project(update, context)
    elif text == '📋 Мои проекты':
        await my_projects(update, context)
    elif text == '👤 Мой профиль':
        await show_profile(update, context)
    elif text == '💡 Создать проект':
        await create_project_start(update, context)
    elif text == '🎯 Рекомендации':
        await show_recommendations(update, context)
    elif text == '❓ Помощь':
        await help_command(update, context)
    elif text == '❌ Отмена':
        await cancel(update, context)
    else:
        await update.message.reply_text(
            "Используйте кнопки меню для навигации",
            reply_markup=get_main_keyboard()
        )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало заполнения профиля"""
    # await update.message.reply_text(
    await update.effective_message.reply_text(
        "Давай заполним твой профиль. Это поможет находить подходящие проекты.\n\n"
        "Кто ты в команде? (Например: разработчик, дизайнер, менеджер и т.д.)",
        reply_markup=get_cancel_keyboard()
    )
    return PROFILE_ROLE

async def profile_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение роли"""
    context.user_data['profile_role'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь напиши свои навыки через запятую.\n"
        "Например: Python, JavaScript, Figma,项目管理,数据分析"
    )
    return PROFILE_SKILLS

async def profile_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение навыков"""
    context.user_data['profile_skills'] = update.message.text
    await update.message.reply_text(
        "Какие у тебя интересы? (Чем хочешь заниматься)\n"
        "Например: веб-разработка, машинное обучение, дизайн интерфейсов"
    )
    return PROFILE_INTERESTS

async def profile_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение интересов"""
    context.user_data['profile_interests'] = update.message.text
    await update.message.reply_text(
        "Расскажи немного о себе (необязательно, можно пропустить):"
    )
    return PROFILE_ABOUT

async def profile_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение информации о себе и завершение"""
    about = update.message.text
    user_id = update.effective_user.id
    
    # Сохраняем профиль в БД
    db.update_user_profile(
        user_id=user_id,
        role=context.user_data.get('profile_role', ''),
        skills=context.user_data.get('profile_skills', ''),
        interests=context.user_data.get('profile_interests', ''),
        about=about
    )
    
    await update.message.reply_text(
        "✅ Профиль успешно сохранен!",
        reply_markup=get_main_keyboard()
    )
    
    return ConversationHandler.END

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать профиль пользователя"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if user and user.get('role'):
        profile_text = (
            f"👤 **Твой профиль**\n\n"
            f"**Роль:** {user.get('role', 'Не указана')}\n"
            f"**Навыки:** {user.get('skills', 'Не указаны')}\n"
            f"**Интересы:** {user.get('interests', 'Не указаны')}\n"
            f"**О себе:** {user.get('about', 'Не указано')}\n"
        )
    else:
        profile_text = "Профиль не заполнен. Нажми '👤 Мой профиль' для заполнения."
    
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✏️ Редактировать профиль", callback_data="edit_profile")
    ]])
    
    await update.message.reply_text(profile_text, parse_mode='Markdown', reply_markup=keyboard)

# Создание проекта
async def create_project_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания проекта"""
    await update.message.reply_text(
        "Давай создадим новый проект!\n\n"
        "Введи название проекта:",
        reply_markup=get_cancel_keyboard()
    )
    return PROJECT_TITLE

async def project_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение названия проекта"""
    context.user_data['project_title'] = update.message.text
    await update.message.reply_text(
        "Опиши проект: цели, задачи, что планируете делать"
    )
    return PROJECT_DESCRIPTION

async def project_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение описания проекта"""
    context.user_data['project_description'] = update.message.text
    
    # Показываем клавиатуру с категориями
    await update.message.reply_text(
        "Выбери категорию проекта:",
        reply_markup=get_categories_keyboard()
    )
    return PROJECT_CATEGORY

async def project_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора категории через callback"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_main":
        await query.edit_message_text("Создание проекта отменено")
        return ConversationHandler.END
    
    category = query.data.replace("cat_", "")
    context.user_data['project_category'] = category
    
    await query.edit_message_text(
        f"Категория: {category}\n\n"
        "Какие навыки нужны для проекта? (перечисли через запятую)\n"
        "Например: Python, React, дизайн, маркетинг"
    )
    return PROJECT_SKILLS

async def project_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение требуемых навыков и создание проекта"""
    skills = update.message.text
    user_id = update.effective_user.id
    
    # Создаем проект в БД
    project_id = db.add_project(
        #title=context.user_data['project_title'],
        title = context.user_data.get('project_title', 'Без названия'),
        description=context.user_data['project_description'],
        category=context.user_data['project_category'],
        required_skills=skills,
        creator_id=user_id
    )
    
    await update.message.reply_text(
        f"✅ Проект успешно создан!\n\n"
        f"ID проекта: {project_id}\n"
        f"Название: {context.user_data['project_title']}\n\n"
        f"Теперь другие пользователи смогут найти его и подать заявки.",
        reply_markup=get_main_keyboard()
    )
    
    return ConversationHandler.END

# Поиск проектов
async def find_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск проектов"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 По категориям", callback_data="find_by_category")],
        [InlineKeyboardButton("🔧 По навыкам", callback_data="find_by_skills")],
        [InlineKeyboardButton("📋 Все проекты", callback_data="all_projects")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]
    ])
    
    await update.message.reply_text(
        "Как хотите искать проекты?",
        reply_markup=keyboard
    )

async def show_projects_list(update: Update, context: ContextTypes.DEFAULT_TYPE, projects: list):
    """Показать список проектов"""
    if not projects:
        await update.message.reply_text("Проекты не найдены")
        return
    
    for project in projects[:5]:  # Показываем по 5 проектов
        project_text = (
            f"📌 **{project['title']}**\n"
            f"📂 Категория: {project['category']}\n"
            f"👤 Создатель: {project['creator_name']}\n"
            f"🔧 Нужны: {project['required_skills']}\n"
            f"📝 {project['description'][:100]}...\n"
            f"🕒 {project['created_at']}"
        )
        
        #is_creator = project['creator_id'] == update.effective_user.id
        if isinstance(update, Update):
            is_creator = project['creator_id'] == update.from_user.id
        else:
            is_creator = project['creator_id'] == update.effective_user.id
        #is_creator = project['creator_id'] == update.callback_query.from_user.id
        keyboard = get_project_actions_keyboard(project['project_id'], is_creator)
        
        await update.message.reply_text(
            project_text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )

# Мои проекты
async def my_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать проекты пользователя"""
    user_id = update.effective_user.id
    projects = db.get_user_projects(user_id)
    
    if not projects:
        await update.message.reply_text(
            "У вас пока нет проектов. Создайте новый или присоединитесь к существующему!"
        )
        return
    
    await update.message.reply_text(f"📋 Найдено проектов: {len(projects)}")
    
    for project in projects:
        role_emoji = "👑" if project['role'] == 'создатель' else "👤"
        status_emoji = "✅" if project['status'] == 'активен' else "⏸"
        
        project_text = (
            f"{role_emoji} **{project['title']}** {status_emoji}\n"
            f"📂 Категория: {project['category']}\n"
            f"📝 {project['description'][:100]}...\n"
            f"Ваша роль: {project['role']}"
        )
        
        await update.message.reply_text(project_text, parse_mode='Markdown')

# Рекомендации
async def show_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать рекомендации проектов"""
    user_id = update.effective_user.id
    recommendations = db.get_recommendations(user_id)
    
    if not recommendations:
        await update.message.reply_text(
            "Не удалось найти рекомендации. Заполните профиль с навыками для лучших результатов!"
        )
        return
    
    await update.message.reply_text(
        f"🎯 Найдено {len(recommendations)} рекомендаций на основе ваших навыков:"
    )
    
    for project in recommendations[:3]:  # Показываем топ-3
        match = project.get('match_percent', 0)
        project_text = (
            f"📌 **{project['title']}**\n"
            f"🎯 Совпадение: {match:.1f}%\n"
            f"📂 Категория: {project['category']}\n"
            f"🔧 Нужны: {project['required_skills']}\n"
            f"👤 Создатель: {project['creator_name']}"
        )
        
        await update.message.reply_text(project_text, parse_mode='Markdown')

# Обработчики callback-запросов
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "fill_profile":
        await profile(query.message, context)
    
    elif data == "edit_profile":
        await profile(query.message, context)
    
    elif data == "find_by_category":
        await query.edit_message_text(
            "Выберите категорию:",
            reply_markup=get_categories_keyboard()
        )
    
    elif data.startswith("cat_"):
        category = data.replace("cat_", "")
        projects = db.get_projects(category=category)
        await show_projects_list(query, context, projects)
    
    elif data == "find_by_skills":
        await query.edit_message_text(
            "Введите навык для поиска (например: Python, дизайн):"
        )
        context.user_data['awaiting_skill'] = True
    
    elif data == "all_projects":
        projects = db.get_projects()
        await show_projects_list(query, context, projects)
    
    elif data.startswith("apply_"):
        project_id = int(data.replace("apply_", ""))
        context.user_data['apply_project_id'] = project_id
        await query.edit_message_text(
            "Напишите сопроводительное сообщение для создателя проекта "
            "(почему вы хотите участвовать, что можете предложить):",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❌ Отмена", callback_data=f"cancel_apply_{project_id}")
            ]])
        )
        return APPLY_MESSAGE
    
    elif data.startswith("applications_"):
        project_id = int(data.replace("applications_", ""))
        applications = db.get_project_applications(project_id)
        
        if not applications:
            await query.edit_message_text("Нет активных заявок")
            return
        
        for app in applications:
            app_text = (
                f"👤 Заявка #{app['application_id']}\n"
                f"От: {app['first_name']} (@{app['username']})\n"
                f"Навыки: {app.get('skills', 'Не указаны')}\n"
                f"Сообщение: {app.get('message', 'Без сообщения')}\n"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Принять", callback_data=f"accept_{app['application_id']}"),
                    InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{app['application_id']}")
                ]
            ])
            
            await query.message.reply_text(app_text, reply_markup=keyboard)
    
    elif data.startswith(("accept_", "reject_")):
        action, app_id = data.split("_")
        app_id = int(app_id)
        
        decision = "принята" if action == "accept" else "отклонена"
        success, message = db.process_application(app_id, decision)
        
        await query.edit_message_text(
            f"✅ Заявка {decision}" if success else f"❌ {message}"
        )
    
    elif data == "back_to_main":
        await query.edit_message_text(
            "Главное меню",
            reply_markup=get_main_keyboard()
        )
    
    elif data == "back_to_projects":
        await query.edit_message_text("Поиск проектов")

async def handle_skill_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка поиска по навыкам"""
    if context.user_data.get('awaiting_skill'):
        skill = update.message.text
        projects = db.get_projects(skill=skill)
        await show_projects_list(update, context, projects)
        context.user_data['awaiting_skill'] = False
    else:
        await handle_message(update, context)

# Отмена действий
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущего действия"""
    context.user_data.clear()
    await update.message.reply_text(
        "Действие отменено",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# Основная функция
def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ConversationHandler для профиля
    profile_conv = ConversationHandler(
        entry_points=[
            CommandHandler('profile', profile),
            CallbackQueryHandler(profile, pattern='^fill_profile$'),
            CallbackQueryHandler(profile, pattern='^edit_profile$')
        ],
        states={
            PROFILE_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_role)],
            PROFILE_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_skills)],
            PROFILE_INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_interests)],
            PROFILE_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_about)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # ConversationHandler для создания проекта
    project_conv = ConversationHandler(
        entry_points=[
            CommandHandler('create', create_project_start),
            MessageHandler(filters.Regex('^💡 Создать проект$'), create_project_start)
        ],
        states={
            PROJECT_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_title)],
            PROJECT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_description)],
            PROJECT_CATEGORY: [CallbackQueryHandler(project_category_callback)],
            PROJECT_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_skills)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # ConversationHandler для подачи заявки
    apply_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern='^apply_')],
        states={
            APPLY_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_apply_message)],
        },
        fallbacks=[CallbackQueryHandler(cancel_apply, pattern='^cancel_apply_')]
    )
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(profile_conv)
    application.add_handler(project_conv)
    application.add_handler(apply_conv)
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_skill_search))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

async def handle_apply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщения заявки"""
    message = update.message.text
    project_id = context.user_data.get('apply_project_id')
    user_id = update.effective_user.id
    
    if project_id:
        success, result = db.join_project(project_id, user_id, message)
        await update.message.reply_text(
            result if not success else "✅ Заявка успешно отправлена!",
            reply_markup=get_main_keyboard()
        )
    
    return ConversationHandler.END

async def cancel_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена подачи заявки"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Подача заявки отменена")
    return ConversationHandler.END

if __name__ == '__main__':
    main()