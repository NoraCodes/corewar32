from flask import request, render_template, session, redirect, url_for, flash

from toroid import app, verify_warriors, database, authentication
from toroid import warrior_dict_relations as wdr
from toroid.error import error_page
from toroid.source import filter_source
from toroid.tournament import num_permutations


# This is the index page, which basically only shows text.
@app.route('/')
def index():
    return render_template('index.html', locked=database.is_db_locked())


# The form for adding a warrior. This passes the data on to later validation
# once the user has entered source code.
@app.route('/add_warrior/')
def add_warrior():
    # If the database is locked, people can't submit new warriors.
    if database.is_db_locked():
        return error_page("The database is locked; submissions are currently \
                          not allowed.")
    # Otherwise, render the form. Not much else to do.
    return render_template('new_warrior.html')


# Logic for checking that the warrior is valid and doesn't already exist in the
# DB. Shows either error or confirmation pages.
@app.route('/verify_warrior/', methods=['POST'])
def verify_warrior():
    # Attempt to get the form data
    inbound_source = request.form.get('source', False)
    if inbound_source is False:
        return error_page("Form data was malformed.", 400)

    # Attempt to verify the submitted program
    (success, output, program_data) = verify_warriors.validate(
                                        filter_source(inbound_source))

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


# The final step of the warrior submission process, this endpoint commits the
# submitted warrior to the database.
@app.route("/commit_warrior/", methods=['POST'])
def commit_warrior():
    # Attempt to get the warrior out of the session
    warrior_dict = session.get('warrior', False)
    # All warriors start with a score of 0
    warrior_dict["score"] = 0
    if warrior_dict is False:
        return error_page('Request was malformed.', 400)

    warrior = wdr.dict_to_warrior(warrior_dict)
    ident = database.add_warrior(warrior)
    flash(('Thank you, {}. Your warrior {} was successfully' +
           ' added to the database as ID #{}.')
          .format(warrior.author, warrior.name, ident))
    return(redirect(url_for('list_warriors')))


# Displays a list of warriors to the user, with admin controls if the user is
# an admin.
@app.route('/list_warriors/')
def list_warriors():
    return render_template('warrior_list.html',
                           programs=database.list_warriors(),
                           admin=authentication.is_authenticated())


# Display a form on GET, do login on POST
# The form is to allow the user to enter the administrator password
# The endpoint for login checks against the serverside config and calls
# blesses the session with magic cow powers
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


# This endpoint unblesses the session, removing any magic cow powers.
@app.route('/logout/')
def logout():
    authentication.logout()
    flash("You have been successfully logged out.")
    return redirect(url_for('index'))

# All routes with a /admin/* kick the user out unceremoneously if the session
# isn't blessed.


# Displays a useful panel of controls for those running a tournament.
@app.route('/admin/')
def admin():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        return render_template('admin.html',
                               n_warriors=len(database.list_warriors_raw()),
                               n_permutations=num_permutations(),
                               locked=database.is_db_locked())
    else:
        return error_page("You are not authorized to access the admin panel.",
                          403)


# Unlocks the database, allowing submissions.
@app.route('/admin/unlock_db')
def unlock_db():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        database.unlock_db()
        flash("Unlocked the database.")
        return redirect(url_for("admin"))
    else:
        return error_page("It's not nice to try and unlock the database " +
                          "without authentication...", 403)


# Locks the database, preventing submissions.
@app.route('/admin/lock_db')
def lock_db():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        database.lock_db()
        flash("Locked the database.")
        return redirect(url_for("admin"))
    else:
        return error_page("It's not nice to try and lock the database " +
                          "without authentication...", 403)


# Purges all entries from the database.
@app.route('/admin/purge_db/')
def purge_db():
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        database.purge_warrior_db()
        flash("Purged the database.")
        return redirect(url_for("admin"))
    else:
        return error_page("It's not nice to try and purge the database " +
                          "without authentication...", 403)


# Deletes a warrior.
@app.route('/admin/delete/', methods=['POST'])
def delete_warrior():
    # Try to get the form data
    name = request.form.get('name', False)
    author = request.form.get('author', False)
    if name is False or author is False:
        return error_page("The request is malformed.", 403)
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        database.delete_warrior_by_name(name)
        flash("Successfully deleted {} by {}.".format(name, author))
        return redirect(url_for('list_warriors'))
    else:
        return error_page("You are not authorized to delete warriors.", 403)


# Displays the source code of a warrior.
@app.route('/admin/acquire/', methods=['POST'])
def acquire_warrior():
    # Try to get the form data
    name = request.form.get('name', False)
    author = request.form.get('author', False)
    if name is False or author is False:
        return error_page("The request is malformed.", 403)
    # Make sure the user is authenticated. If not, kick them out.
    if authentication.is_authenticated():
        warrior = database.get_warrior_by_name(name)
        return render_template("retrieve.html", warrior=warrior)
    else:
        return error_page("You are not authorized to access the source code " +
                          "of warriors.", 403)


# Makes pairings and places them in the session
# DEPRECATED
@app.route('/admin/pair/')
def pair_warriors():
    from toroid.pairs import make_pairings
    # Check if we're authenticated
    if authentication.is_authenticated():
        # Try to pair all the warriors in the db
        (raw_pairs, raw_odd_one_out) = make_pairings(
                                    database.list_warriors_raw())
        # See if we got back pairings
        if raw_pairs is False:
            return error_page("Pairing failed. Are there warriors in the db?",
                              500)
        # Place results in the session
        session['raw_pairs'] = raw_pairs
        session['raw_odd_one_out'] = raw_odd_one_out
        return redirect(url_for('show_pairs'))
    else:
        return error_page("You are not authorized to generate pairs.", 403)


# Displays pairs.
# DEPRECATED
@app.route('/admin/show_pairs')
def show_pairs():
    if authentication.is_authenticated():
        # Try and get data from the session
        raw_pairs = session.get('raw_pairs', False)
        raw_odd_one_out = session.get('raw_odd_one_out', None)
        if raw_pairs is False or raw_odd_one_out is None:
            return error_page("Your pair data is invalid. Regenerate.", 400)

        # We have data, convert it.
        pairs = wdr.dictpairlist_to_warriorpairlist(raw_pairs)
        if raw_odd_one_out is not False:
            odd_one_out = wdr.dict_to_warrior(raw_odd_one_out)
        else:
            odd_one_out = False

        # OK! Render.
        return render_template('pairs.html',
                               pairs=pairs,
                               odd_one_out=odd_one_out)

    else:
        return error_page("You're not allowed to make pairs. You can't " +
                          "have any to view... why are you here?", 500)
