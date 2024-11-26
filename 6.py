from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Создаем экземпляр приложения Flask
app = Flask(__name__)  # Исправлено на __name__ для корректной работы приложения
app.secret_key = 'key'  # Секретный ключ для сессий
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'  # Конфигурация базы данных с использованием SQLite
db = SQLAlchemy(app)  # Инициализация SQLAlchemy

# Хранение пользователей и паролей в виде словаря
users = {'user': 'password'}  # username: password

# Модель данных для статистики пользователей
class UserStatistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    username = db.Column(db.String(100), nullable=False)  # Имя пользователя
    message_count = db.Column(db.Integer, default=0)  # Счетчик сообщений
    command_count = db.Column(db.Integer, default=0)  # Счетчик команд
    last_active = db.Column(db.DateTime, default=datetime.utcnow)  # Время последней активности

# Модель данных для использования команд
class CommandUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    command_name = db.Column(db.String(100), nullable=False)  # Название команды
    usage_date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата использования команды
    count = db.Column(db.Integer, default=0)  # Счетчик использования команды

# Создание базы данных, если она еще не существует
with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def home():
    return render_template('home1.html')  # Отображение главной страницы

# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html')  # Отображение страницы "О нас"

# Страница галереи
@app.route('/gallery')
def gallery():
    # Список изображений для отображения в галерее
    images = [
        'cat1.jpg',
        'cat2.jpg',
        'cat3.jpg',
        'cat4.jpg',
        'cat5.jpg',
        'cat6.jpg'
    ]
    return render_template('gallery.html', images=images)  # Отображение галереи

# Страница авторизации
@app.route('/author', methods=['GET', 'POST'])
def author():
    if request.method == 'POST':  # Обработка POST-запроса
        username = request.form['username']  # Получение имени пользователя из формы
        password = request.form['password']  # Получение пароля из формы
        if users.get(username) == password:  # Проверка корректности логина и пароля
            session['username'] = username  # Сохранение имени пользователя в сессии

            # Добавляем или обновляем статистику пользователя
            user_stats = UserStatistics.query.filter_by(username=username).first()  # Поиск статистики пользователя
            if not user_stats:  # Если статистики нет, создаем новую запись
                user_stats = UserStatistics(username=username)
            user_stats.last_active = datetime.utcnow()  # Обновляем время последней активности
            user_stats.message_count += 1  # Увеличиваем счетчик сообщений
            db.session.add(user_stats)  # Добавляем объект в сессию
            db.session.commit()  # Сохраняем изменения в базе данных

            return redirect(url_for('home'))  # Перенаправление на главную страницу
        else:
            return 'Неверный логин или пароль', 401  # Ошибка при неверных данных
    return render_template('author.html')  # Отображение страницы авторизации

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('username', None)  # Удаление имени пользователя из сессии
    return redirect(url_for('home'))  # Перенаправление на главную страницу

# Обработка сообщения
@app.route('/message', methods=['POST'])
def message():
    # Обрабатываем сообщение и увеличиваем счетчик сообщений для пользователя
    if 'username' in session:  # Проверка авторизации
        username = session['username']  # Получение имени пользователя из сессии
        user_stats = UserStatistics.query.filter_by(username=username).first()  # Получение статистики пользователя
        if user_stats:
            user_stats.message_count += 1  # Увеличиваем счетчик сообщений
            db.session.commit()  # Сохраняем изменения
    return jsonify(success=True)  # Возвращаем JSON-ответ о успешном выполнении

# Обработка команды
@app.route('/command/<command>', methods=['POST'])
def execute_command(command):
    # Увеличиваем счетчик использования команды
    if 'username' in session:  # Проверка авторизации
        username = session['username']  # Получение имени пользователя из сессии
        user_stats = UserStatistics.query.filter_by(username=username).first()  # Получение статистики пользователя
        if user_stats:
            user_stats.command_count += 1  # Увеличиваем счетчик команд
            db.session.commit()  # Сохраняем изменения

        command_usage = CommandUsage.query.filter_by(command_name=command, usage_date=datetime.utcnow().date()).first()  # Поиск использования команды
        if command_usage:  # Если использование команды уже зарегистрировано
            command_usage.count += 1  # Увеличиваем счетчик
        else:
            command_usage = CommandUsage(command_name=command, count=1)  # Создаем новую запись
        db.session.add(command_usage)  # Добавляем объект в сессию
        db.session.commit()  # Сохраняем изменения

    return jsonify(success=True)  # Возвращаем JSON-ответ о успешном выполнении

# Страница со статистикой
@app.route('/stats')
def stats():
    user_stats = UserStatistics.query.all()  # Получение всех статистик пользователей
    command_stats = CommandUsage.query.all()  # Получение всех данных о использовании команд

    return render_template('stats.html', user_stats=user_stats, command_stats=command_stats)  # Отображение страницы статистики

# Запуск приложения
if __name__ == '__main__':  # Проверка, запускается ли скрипт напрямую
    app.run(debug=True)  # Запуск приложения с режимом отладки
