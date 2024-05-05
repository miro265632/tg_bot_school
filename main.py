import os
import datetime as dt
from requests import get
from dotenv import load_dotenv
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup




from tg_bot_school.ORM_test.data import db_session
from tg_bot_school.ORM_test.data.users import User

TOKEN = '6657157411:AAGEdLK_C6n_FVTnEqmOqwI0zPZJeesu2KE'

db_session.global_init("ORM_test/db/Users.db")

username = ''

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reply_keyboard = [["/add"], ["/replace"], ["/delete"], ['/show'], ["/start"], ["/stop"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def info_func(update, context):
    await update.message.reply_html('<b>/add</b> - '
                                    'Добавление данных в таблицу')
    await update.message.reply_html('<b>/replace</b> - '
                                    'Замена данных в таблице')
    await update.message.reply_html('<b>/delete</b> - '
                                    "Удаление данных из таблицы")
    await update.message.reply_html('<b>/show</b> - '
                                    "Просмотр данных в таблице")
    await update.message.reply_html('<b>/start</b> - '
                                    "При нажатии этой кнопке Вы просто начнете сначало")
    await update.message.reply_html('<b>/stop</b> - '
                                    "При нажатии этой кнопки бот остановится")
    await update.message.reply_html('Выберите одну из представленных функций')




async def stop(update, context):

    user = update.effective_user
    await update.message.reply_text(f"Пока!")
    return ConversationHandler.END


async def add(update, context):
    await update.message.reply_html('Введите данные, которые вы хотите добавить в таблицу в формате'
                                    ' "Имя Фамилия возраст" (через пробел)')
    return 1


async def add_response(update, context):
    global username
    user = update.effective_user

    username = user['username']
    data = update.message.text.split()
    db_sess = db_session.create_session()
    if data[2].isdigit():

        user = User(username=username, name=data[0].title(), surname=data[1].title(), age=data[2])
        db_sess.add(user)
        db_sess.commit()
        await update.message.reply_text('Ваши данные добавлены в таблицу')
    else:
        await update.message.reply_text('В значении возраста должна быть цифра!')




    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def replace(update, context):
    await update.message.reply_html('Введите id пользователя, у которого хотите изменить информацию (цифра перед именем)\n'
                                    'Введите параметр изменений (имя, фамилия, возраст)\n'
                                    'Введите данные для изменений')
    return 3


async def replace_response(update, context):
    global username
    db_sess = db_session.create_session()
    data = update.message.text.split()
    user = update.effective_user
    print(data[1])
    username = user['username']
    user = db_sess.query(User).filter(User.id == data[0]).first()
    if data[1].lower()=='имя':
        user.name=data[2]
        await update.message.reply_text('Данные успешно изменены')
    elif data[1].lower()=='фамилия':
        user.surname=data[2]
        await update.message.reply_text('Данные успешно изменены')
    elif data[1].lower()=='возраст':
        if data[2].isdigit():
            user.age=data[2]
            await update.message.reply_text('Данные успешно изменены')
        else:
            await update.message.reply_text('В значении возраста должна быть цифра!')
    else:
        await update.message.reply_text('Такого параметра нет в таблице')

    db_sess.commit()


    return ConversationHandler.END


conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('replace', replace)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, replace_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])


async def delete(update, context):
    await update.message.reply_html('Введите id пользователя, данные которого хотите удалить изх таблицы ')
    return 5


async def delete_response(update, context):
    global username
    db_sess = db_session.create_session()
    locality = update.message.text
    user = update.effective_user
    username = user['username']
    user = db_sess.query(User).filter(User.id == locality).first()

    db_sess.delete(user)
    db_sess.commit()


    await update.message.reply_text('Данные пользователя удалены')
    return ConversationHandler.END


conv_handler3 = ConversationHandler(
    entry_points=[CommandHandler('delete', delete)],
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        5: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_response)]

    },
    fallbacks=[CommandHandler('stop', stop)])

async def show(update, context):
    global username
    print('sas')
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    for user in db_sess.query(User).all():
        await update.message.reply_html(f'{user.id}. {user.name} {user.surname}, {user.age}')
    db_sess.commit()
    return ConversationHandler.END


async def start(update, context):
    user = update.effective_user
    global username
    username = user['username']

    db_sess = db_session.create_session()

    user_bd = db_sess.query(User).filter(User.username == username).first()
    if not user_bd:

        await update.message.reply_html(
            rf'Привет, {user.mention_html()}! Нажми на /info_func, чтобы узнать мой функционал' rf'',
            reply_markup=markup)

    else:
        await update.message.reply_html(
            rf'Привет,{user.mention_html()}! Рады видеть тебя снова. Выбери интересующую функцию)' rf'',
            reply_markup=markup)





def main():
    token = os.environ.get('TOKEN', '')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(conv_handler)
    app.add_handler(conv_handler2)
    app.add_handler(conv_handler3)

    app.add_handler(CommandHandler('add', add))
    app.add_handler(CommandHandler('replace', replace))
    app.add_handler(CommandHandler('delete', delete))
    app.add_handler(CommandHandler('show', show))
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('info_func', info_func))

    app.run_polling()


if __name__ == '__main__':
    main()