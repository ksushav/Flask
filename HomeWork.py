from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
db = SQLAlchemy(app)

users = {'user': 'password'}

class UserStatistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    message_count = db.Column(db.Integer, default=0)
    command_count = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

class CommandUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command_name = db.Column(db.String(100), nullable=False)
    usage_date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    cards = [
        {"title": "Фоточка 1", "description": "Котик с помидоркой", "img": "static/images/card1.jpg"},
        {"title": "Фоточка 2", "description": "Довольная девушка с недовольной кошкой (Мотя (Матильда))", "img": "static/images/card2.jpg"},
        {"title": "Фоточка 3", "description": "Он смешон", "img": "static/images/card3.jpg"},
    ]

    accordion_content = [
        {"header": "Где искать картинки с котиками?", "body": """
        Вот несколько популярных ресурсов, где вы можете найти картинки со смешными котиками:

1. Поисковые системы:

   Google Images: Просто введите «смешные котики» в поисковую строку и выберите раздел «Изображения». Используйте фильтры для поиска изображений с разрешением, которое вам нужно.

   Bing Images: Аналогично Google, Bing также предлагает поиск изображений.

2. Стоковые фото:

   Unsplash: Бесплатные высококачественные изображения, включая фотографии котиков.

   Pexels: Еще один ресурс с бесплатными стоковыми фотографиями, где можно найти множество изображений котиков.

   Shutterstock или Adobe Stock: Платные ресурсы с большим выбором профессиональных фотографий.

3. Социальные сети:

   Instagram: Используйте хештеги, такие как #funnycats или #catsofinstagram, чтобы найти смешные картинки.

   Pinterest: Здесь можно найти множество коллекций с изображениями котиков.

4. Мем-ресурсы:

   Imgur: Популярный сайт для обмена изображениями, где часто публикуются мемы с котиками.

   Reddit: Подреддиты, такие как r/cats или r/catmemes, полны смешных картинок с котами.

5. Специальные сайты:

   Cats of Instagram: Сайт, посвященный котикам из Instagram.

   The Cat Gallery: Сайт с коллекцией смешных и милых котиков.

Не забывайте проверять лицензию на использование изображений, особенно если вы планируете использовать их в коммерческих целях!"""},
        {"header": "Как искать картинки с котиками?", "body": """
Выбор самых смешных картинок с котиками может быть субъективным, так как чувство юмора у каждого свое. Тем не менее, вот несколько советов, как найти и выбрать действительно забавные изображения:

1. Используйте специализированные сайты и приложения:

   Сайты вроде Reddit (подфорумы, такие как r/cats или r/catpictures) часто содержат множество смешных картинок с котами.

   Instagram и Pinterest также являются отличными платформами для поиска смешных изображений.

2. Поиск по ключевым словам:

   Используйте поисковые системы (например, Google Images) и вводите запросы вроде "смешные котики", "котики мемы" или "милые котики".

3. Обратите внимание на популярность:

 Изучите количество лайков, комментариев и репостов на социальных платформах. Чем больше взаимодействий, тем вероятнее, что картинка смешная.

4. Фильтруйте по типу юмора:

   Учитывайте свой вкус. Вам могут нравиться котики в смешных позах, с забавными выражениями лиц или в необычных ситуациях.

5. Соберите коллекцию:

   Создайте папку на своем устройстве или в облачном хранилище, куда вы будете собирать картинки, которые вас развеселили.

6. Обратите внимание на мемы:

    Мемы с котиками часто становятся вирусными и могут быть очень смешными. Поиск по популярным мемам может привести к интересным находкам.

7. Делитесь с друзьями:

   Попросите друзей поделиться своими любимыми картинками с котиками. Это может привести к новым и смешным находкам.

8. Участвуйте в сообществах:

    Присоединяйтесь к группам в социальных сетях или форумах, посвященным котикам и юмору. Там часто публикуются самые смешные картинки.

Надеюсь, эти советы помогут вам найти много смешных картинок с котиками!
"""},
        {"header": "Что делать с картинками с котиками?", "body": """1. Использование в социальных сетях\n

Вы можете использовать картинки с котиками для создания постов в социальных сетях. Просто загрузите изображение и добавьте к нему текст или хештеги.\n

2. Создание презентаций\n

Если вы создаете презентацию, вы можете вставить картинки с котиками в слайды, чтобы сделать их более привлекательными и интересными.\n

3. Вставка в документы\n

Вы можете вставить картинки с котиками в текстовые документы (например, Word или Google Docs), просто скопировав и вставив изображение.\n

4. Использование в играх или приложениях\n

Если вы разрабатываете игру или приложение, вы можете использовать изображения котиков в качестве спрайтов или фонов.\n"""},
    ]

    return render_template('home.html', cards=cards, accordion_content=accordion_content)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    images = ['cat1.jpg', 'cat2.jpg', 'cat3.jpg', 'cat4.jpg', 'cat5.jpg', 'cat6.jpg']
    return render_template('gallery.html', images=images)

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

@app.route('/logout')
def logout():
    session.pop('username', None)  # Удаление имени пользователя из сессии
    return redirect(url_for('home'))  # Перенаправление на главную страницу

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

@app.route('/stats')
def stats():
    user_stats = UserStatistics.query.all()
    command_stats = CommandUsage.query.all()
    return render_template('stats.html', user_stats=user_stats, command_stats=command_stats)

if __name__ == '__main__':
    app.run(debug=True)