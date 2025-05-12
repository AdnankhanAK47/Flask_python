from flask import Flask
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable= False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref = 'user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False)
    content = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')    

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect('/')

@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id = current_user.id).all()
    return render_template ('task_list.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/add', methods=['POST'])
@login_required
def add():
    content=request.form['content']
    New_task=Task(content=content, user_id = current_user.id)
    db.session.add(New_task)
    db.session.commit()
    return redirect('/')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

@app.route("/about")
def about():
    return render_template('about.html', name = "mohd adnan khan", contact = 6301433748, email = "mohdadnan78619@gmail.com" )

@app.route('/user/<username>')
def user_profile(username):
    return render_template ('user.html', username=username)

@app.route('/square/<int:number>')
def square(number):
    result = number * number
    return f"The Square root of {number} is {result}."

@app.route("/contact")
def contact():
    number = 6301433748
    return f"if any Quaries related to this website please contact The number Given Below \n {number}"

@app.route("/Services")
def Services():
    return "We Offer Web Development\nLike 1. Data Analsis\n2. Python\n3. automation services "

@app.route("/Services/<service_name>")
def show_Services(service_name):
    return f"You Selected the {service_name.capitalize()} Service."

@app.route("/multiply/<int:a>*<int:b>")
def multiply(a,b):
    return f"{a} * {b} = {a*b}"

@app.route("/form", methods = ['GET', 'POST'])
def form():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        print("username submitted:", username)
        print("Email submitted:", email)
        return render_template('greet.html', username=username, email=email)
    return render_template('form.html')
if __name__ == '__main__':
    app.run(debug=True)