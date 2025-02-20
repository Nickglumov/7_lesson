import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло")


def wait(chat_id, question):
    delay = parse(question)
    message_id = bot.send_message(chat_id, f"Таймер установлен на {delay} секунд")
    bot.create_countdown(delay, notify_progress, chat_id=chat_id, message_id=message_id, total_time=delay)
    bot.create_timer(delay, notify, chat_id=chat_id)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, total_time):
    progress_bar = render_progressbar(total_time, total_time - secs_left, prefix="Прогресс:", suffix="Завершено", length=30)
    bot.update_message(chat_id, message_id, f"Осталось секунд: {secs_left}\n{progress_bar}")


def main():
    global bot
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main()
