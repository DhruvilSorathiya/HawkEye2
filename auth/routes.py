from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import auth_bp, login_manager, mail
from .models import db, User, Activity, PasswordResetToken
from .forms import LoginForm, UserCreationForm, AdminCreationForm, ForgotPasswordForm, ResetPasswordForm
from .utils import send_reset_email, generate_token, token_expiry
from datetime import datetime

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def log_activity(user, action):
    activity = Activity(user_id=user.id, action=action)
    db.session.add(activity)
    db.session.commit()

@auth_bp.route('/login_select', methods=['GET'])
def login_select():
    return render_template('login_select.html')

@auth_bp.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if role not in ['user', 'admin']:
        flash("Invalid login role.", "danger")
        return redirect(url_for('auth.login_select'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, role=role).first()
        if user and user.check_password(form.password.data) and user.is_approved:
            login_user(user)
            log_activity(user, "Logged in")
            if role == 'admin':
                return redirect(url_for('auth.admin_dashboard'))
            else:
                # If you have a main.index route, adjust this as needed
                return redirect('/newscan')  # or url_for('main.index') if you have a main blueprint
        else:
            flash('Invalid credentials or account not approved.', 'danger')
    return render_template(f'login_{role}.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    log_activity(current_user, "Logged out")
    logout_user()
    return redirect(url_for('auth.login_select'))

@auth_bp.route('/forgot_password/<role>', methods=['GET', 'POST'])
def forgot_password(role):
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role=role).first()
        if user:
            token = generate_token()
            expiry = token_expiry()
            reset_token = PasswordResetToken(token=token, user_id=user.id, expiry=expiry)
            db.session.add(reset_token)
            db.session.commit()
            send_reset_email(user, token, mail)
            flash('Check your email for password reset instructions.', 'info')
        else:
            flash('No account found with this email.', 'danger')
    return render_template('forgot_password.html', form=form, role=role)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
    if not reset_token or reset_token.expiry < datetime.utcnow():
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login_select'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = reset_token.user
        user.set_password(form.password.data)
        db.session.commit()
        reset_token.used = True
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('auth.login_select'))
    return render_template('reset_password.html', form=form)

@auth_bp.route('/admin/register', methods=['GET', 'POST'])
def register_admin():
    form = AdminCreationForm()
    admins = User.query.filter_by(role='admin').count()
    if admins == 0:  # First admin can self-register
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, role='admin', is_approved=True)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Admin account created. Please log in.', 'success')
            return redirect(url_for('auth.login', role='admin'))
    else:
        # Only existing users can approve a new admin
        flash('Admin account creation requires approval from a user.', 'warning')
        return redirect(url_for('auth.login_select'))
    return render_template('register_admin.html', form=form)

@auth_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login_select'))
    users = User.query.filter(User.role == 'user').all()
    return render_template('admin_dashboard.html', users=users)

@auth_bp.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login_select'))
    form = UserCreationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, mobile=form.mobile.data, role='user', is_approved=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('auth.admin_dashboard'))
    return render_template('create_user.html', form=form)

@auth_bp.route('/admin/users/<int:user_id>/activity')
@login_required
def user_activity(user_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login_select'))
    user = User.query.get_or_404(user_id)
    activities = Activity.query.filter_by(user_id=user.id).order_by(Activity.timestamp.desc()).all()
    return render_template('user_activity.html', user=user, activities=activities)