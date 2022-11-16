from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from models import Users, db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Register Route
@auth.route('/register', methods=('GET', 'POST'))
def register():
    msg = ''
    if request.method == 'POST':
        logout_user()
        name = request.form['name']
        passcode = request.form['passcode']
        
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = Users(name=name, passcode=passcode)
        
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Thank you for registering your account, please login!')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html',  msg=msg, name='Contact App - Register')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    msg = ''
    if request.method == 'POST' and 'passcode' in request.form:
        passcode = request.form['passcode']
        
        user = Users.query.filter_by(passcode=passcode).first()
        
        if user is None:
            msg = "User with that passcode dosnt exist."
        else:
            login_user(user, remember=True)
            return redirect(url_for('index'))
            
        print(msg)

    return render_template('auth/login.html', msg=msg, name='Contact App - Login')
   

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
