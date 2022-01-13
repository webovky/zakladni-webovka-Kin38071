from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
"""
*   secret key se generuje nejlépe pomocí os.urandom(24)
*   ale obecně to je prostě velké náhodné číslo
*   proměnnou secret_key nikdy nikdy nikdy nesdílím v repositáři!!! tak jako teď
"""
app.secret_key = b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash(f'Pro zobrazení této stránky ({request.path}) je nutné se přihlásit', 'err')
            return redirect(url_for('login', next=request.path))
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper


@app.route("/")
def index():
    return render_template("base.html.j2", a=12, b=3.14)


@app.route("/python/", methods=["GET"])
def python():
    return render_template("python.html.j2")

@app.route("/rust/", methods=["GET"])
@login_required
def rust():
    return render_template("rust.html.j2")


@app.route("/holyc/")
@login_required
def holyc():
    return render_template("holyc.html.j2")

@app.route("/login/", methods=['GET'])
def login():
    login = request.args.get('nick')
    passwd = request.args.get('pswd')
    return render_template("login.html.j2")

@app.route("/login/", methods=['POST'])
def login_post():
    login = request.form.get('nick')
    passwd = request.form.get('pswd')
    next = request.args.get('next')
    if passwd == 'lokomotiva' :
        session['user'] = login
        flash("Úspěšně jste se přihlásil!", 'pass')
        if next:
            return redirect(next)
    else:
        flash("Špatné přihlašovací údaje!", 'err')
    if next:
        return redirect(url_for("login", next=next))
    else:
        return redirect(url_for('login'))

@app.route("/logout/")
def logout():
    session.pop('user', None)
    flash("Právě jsi se odhlásil", 'pass')
    return redirect(url_for('login'))