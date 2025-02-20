from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

from config import TOKEN

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Хранилище заметок (временное, в реальном приложении можно использовать базу данных)
notes = {}

# Команда для добавления заметки
async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    note = ' '.join(context.args)  # Получаем текст заметки из аргументов

    if chat_id not in notes:
        notes[chat_id] = []

    if note:
        notes[chat_id].append(note)
        await update.message.reply_text(f'Заметка добавлена: "{note}"')
    else:
        await update.message.reply_text('Пожалуйста, укажите текст заметки.')

# Команда для просмотра всех заметок
async def view_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id in notes and notes[chat_id]:
        all_notes = '\n'.join(notes[chat_id])
        await update.message.reply_text(f'Ваши заметки:\n{all_notes}')
    else:
        await update.message.reply_text('У вас нет заметок.')

# Команда для удаления заметки
async def delete_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id in notes and notes[chat_id]:
        try:
            index = int(context.args[0]) - 1  # Индекс заметки (пользователь вводит с 1)
            if 0 <= index < len(notes[chat_id]):
                removed_note = notes[chat_id].pop(index)
                await update.message.reply_text(f'Заметка удалена: "{removed_note}"')
            else:
                await update.message.reply_text('Некорректный номер заметки.')
        except (IndexError, ValueError):
            await update.message.reply_text('Пожалуйста, укажите номер заметки для удаления.')
    else:
        await update.message.reply_text('У вас нет заметок.')

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("add_note", add_note))
    application.add_handler(CommandHandler("view_notes", view_notes))
    application.add_handler(CommandHandler("delete_note", delete_note))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())