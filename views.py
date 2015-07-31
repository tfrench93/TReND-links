import forms
import models
from app import app
from flask import render_template, redirect, flash, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (login_required, login_user, logout_user,
                            current_user)

@app.route('/user/<nickname>')
def user_profile(nickname):
    user = models.User.get(models.User.nickname == nickname)
    if not user:
        flash('User could not be found.')
    else:
        profile = models.UserProfile.get(models.UserProfile.user == user)
    return render_template(
        'user_profile.html', 
        profile=profile,
        user=user)

@app.route('/register', methods=('GET', 'POST'))
def register():
  form = forms.RegistrationForm()
  if form.validate_on_submit():
    flash('Yay! You registered.', 'success')
    models.User.create_user(
        email=form.email.data,
        password=form.password.data)
    return redirect(url_for('index'))
  return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
  form = forms.LoginForm()
  if form.validate_on_submit():
    try:
      user = models.User.get(models.User.email == form.email.data)
    except models.DoesNotExist:
      flash("Your email or password doesn't match.", 'error')
    else:
      if check_password_hash(user.password, form.password.data):
        login_user(user)
        flash("You've been successfully logged in!", 'success')
        return redirect(url_for('index'))
      else:
        flash("Your email or password doesn't match.", 'error')
  return render_template('login.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash("You've been logged out.", 'success')
  return redirect(url_for('index'))

@app.route('/')
def index():
  return render_template('index.html')

