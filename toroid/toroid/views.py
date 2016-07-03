from flask import request, render_template, session, redirect, url_for

from toroid import app, verify_warriors, database, authentication
from toroid.error import error_page


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_warrior/')
def add_warrior():
    return error_page("Adding warriors is not implemented.", 500)

@app.route('/list_warriors/')
def list_warriors():
    return error_page("Listing warriors is not supported.")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # If we don't have form data, simply show the form or the admin page.
    if request.method == 'GET':
        if authentication.is_authenticated():
            return redirect(url_for('admin'))
        else:
            return render_template('login.html')

    # If we do have form data, validate the password and take the appropriate
    #   action
    if request.method == 'POST':
        password = request.form.get('password', '')
        if authentication.check_password(password):
            authentication.login()
            return redirect(url_for('login'))
        else:
            return error_page('The password was incorrect.', 403)

@app.route('/admin/')
def admin():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        return error_page("Admin panel is not implemented.", 500)
    else:
        return error_page("You are not authorized to access the admin panel.",
                          403)
