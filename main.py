from flask import *
import json
import os
import requests
from datetime import datetime
import telebot

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-12345-!@#$%')

# === Настройки Telegram (можно убрать, если не нужна отправка) ===
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8461294572:AAHIgI2Sm5zHHXotwVTjoMkkbOJGEn-cAj0')  # лучше через .env или переменные окружения
CHAT_IDS = os.getenv('TELEGRAM_CHAT_IDS', '839519148,5362530571,110508270').split(',')  # например: "123456789,987654321"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)

# Путь к JSON-файлу
DATA_FILE = 'submissions.json'

RECAPTCHA_SECRET_KEY = '6LfNOdkrAAAAALe1bxVSwC3yLSHwbTpfgp5ifByt'

def verify_recaptcha(response_token):
    if not response_token:
        return False
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = r.json()
    return result.get('success', False)

def save_to_json(data):
    """Сохраняет данные в JSON-файл (добавляет в массив)"""
    submissions = []

    # Пытаемся прочитать существующие данные
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                submissions = json.load(f)
                # Убедимся, что это список
                if not isinstance(submissions, list):
                    submissions = []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Предупреждение: файл {DATA_FILE} повреждён или недоступен. Создаём новый.")
            submissions = []

    # Добавляем новую запись
    submissions.append(data)

    # Записываем обратно (файл будет создан, если не существует)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Ошибка записи в файл {DATA_FILE}: {e}")
        raise

def send_telegram_notification(data):
    if not TELEGRAM_BOT_TOKEN or not CHAT_IDS:
        return

    text = f"""
🔔 Новая заявка на сайте!

Имя: {data['name']}
Телефон: {data['phone']}
Сообщение: {data.get('message', '—')}

Время: {data['timestamp']}
    """.strip()

    for chat_id in CHAT_IDS:
        chat_id = chat_id.strip()
        if chat_id:
            try:
                bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
            except Exception as e:
                print(f"Ошибка отправки в Telegram через telebot: {e}")

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()
    consent = request.form.get('consent')
    recaptcha_response = request.form.get('g-recaptcha-response')

    if not verify_recaptcha(recaptcha_response):
        flash("Пожалуйста, подтвердите, что вы не робот.", "error")
        return redirect(url_for('index'))

    if not name or not phone or not consent:
        flash("Все поля обязательны для заполнения.", "error")
        return redirect(url_for('index'))

    submission = {
        'timestamp': datetime.now().isoformat(),
        'name': name,
        'phone': phone,
        'message': message
    }

    try:
        save_to_json(submission)
        send_telegram_notification(submission)
        flash("Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.", "success")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        flash("Произошла ошибка при отправке заявки. Попробуйте позже.", "error")

    return redirect(url_for('index'))


#Main page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/nalogovaya-proverka')
def provNalog():
    return render_template("nalogovaya-proverka.html")

@app.route('/donachisleniya-nalogov')
def donachisleniyaNalogov():
    return render_template("donachisleniya-nalogov.html")

@app.route('/blokirovka-schetov')
def blokirovkaSchetov():
    return render_template("blokirovka-schetov.html")

@app.route('/nalogovaya-otvetstvennost')
def nalogovayaOtvetstvennost():
    return render_template("nalogovaya-otvetstvennost.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/cases')
def cases():
    return render_template("cases.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/sitemap.xml')
def sitemap():
    return render_template("sitemap.xml")

@app.route('/robots.txt')
def robotstxt():
    return render_template("robots.txt")

if __name__ == '__main__':
    app.run(debug=False)
