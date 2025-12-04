from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
    session,
)
from flask_wtf.csrf import CSRFProtect
from forms import ContactForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
csrf = CSRFProtect(app)
app.debug = True
app.config['SECRET_KEY'] = (
    'a-really-really-really-long-secret-key-this-in-production'
)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///D:/Dev/flask_my_project/flask_app/SQLite.db'
)
# Отключение отслеживания модификаций (экономит память)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Показывает SQL-запросы в консоли (для отладки)
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html', name='Jerry')


@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)


@app.route('/books/<genre>/')
def books(genre):
    return "All Books in {} category".format(genre)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Используем форму из Flask-WTF
    message = ''

    if form.validate_on_submit():  # Проверяет и CSRF, и валидацию данных
        username = form.username.data
        password = form.password.data

        if username == 'root' and password == 'pass':
            message = "Correct username and password"
            # Здесь незабыть сделать переход на ввод картинок login_user() и redirect
        else:
            message = "Wrong username or password"

    return render_template('login.html', form=form, message=message)


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        print("Data received. Now redirecting ...\n")
        flash("Message Received", "success")
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Value of cookie foo is {}".format(request.cookies.get('foo'))
        )
    return res


@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res


@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = (
            session.get('visits') + 1
        )  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    return "Total visits: {}".format(session.get('visits'))


@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'


@app.route('/session/')
def updating_session():
    res = str(session.items())
    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}

    if 'cart_item' in session:
        session['cart_item']['pineapples'] = '100'
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='category')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


# @app.cli.command("create-db")
# def create_db_command():
#     """Создать базу данных"""
#     with app.app_context():
#         db.create_all()
#         print("✅ База данных создана!")
#         print(f"📁 Файл: {app.config['SQLALCHEMY_DATABASE_URI']}")


if __name__ == "__main__":
    with app.app_context():
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        if not inspector.get_table_names():  # Если таблиц нет
            db.create_all()
            print("База данных инициализирована")
        else:
            print("База данных уже существует")
    app.run(debug=True)
