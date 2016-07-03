from flask import request, render_template, session, redirect, url_for

from toroid import app, verify_warriors, database, authentication
from toroid import warrior_dict_relations as wdr
from toroid.error import error_page
from toroid.success import success_page


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_warrior/')
def add_warrior():
    return render_template('new_warrior.html')


@app.route('/verify_warrior/', methods=['POST'])
def verify_warrior():
    # Attempt to get the form data
    inbound_source = request.form.get('source', False)
    if inbound_source is False:
        return error_page("Form data was malformed.", 400)

    # Attempt to verify the submitted program
    (success, output, program_data) = verify_warriors.validate(inbound_source)

    if not success:
        return error_page("Submission failed to validate. <br> <pre>{}</pre>"
                          .format(output))

    # Reaching this point means that we have a valid program. Now to check
    #   if a program with the same name or author already exists.
    if database.get_warrior_by_name(program_data.name):
        return error_page("A warrior named {} already exists."
                          .format(program_data.name))
    if database.get_warrior_by_author(program_data.author):
        return error_page(("A warrior by {} already exists. You may " +
                           "submit only one warrior to each competition. " +
                           "If you submitted a warrior in error, please " +
                           "contact the event staff to have it removed from " +
                           "the system.").format(program_data.author))
    # We can place it in the session and move on to commission, if the user
    #   so desires.
    session['warrior'] = wdr.warrior_to_dict(program_data)

    return render_template('verify_warrior.html',
                           message=output,
                           name=program_data.name,
                           author=program_data.author,
                           success=success)


@app.route("/commit_warrior/", methods=['POST'])
def commit_warrior():
    # Attempt to get the warrior out of the session
    warrior_dict = session.get('warrior', False)
    if warrior_dict is False:
        return error_page('Request was malformed.', 400)

    warrior = wdr.dict_to_warrior(warrior_dict)
    ident = database.add_warrior(warrior)
    return success_page(('Thank you, {}. Your warrior {} was successfully' +
                        ' added to the database as ID #{}.')
                        .format(warrior.author,
                                warrior.name,
                                ident))


@app.route('/list_warriors/')
def list_warriors():
    return render_template('warrior_list.html',
                           programs=database.list_warriors())


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


@app.route('/logout/')
def logout():
    authentication.logout()
    return redirect(url_for('index'))


@app.route('/admin/')
def admin():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        return render_template('admin.html')
    else:
        return error_page("You are not authorized to access the admin panel.",
                          403)


@app.route('/delete/', methods=['POST'])
def delete_warrior():
    return error_page("Deletion is not implemented.", 500)


@app.route('/acquire/', methods=['POST'])
def acquire_warrior():
    return error_page("Source acquisition is not implemented.", 500)
