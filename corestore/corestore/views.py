from flask import request, render_template, session
from uuid import uuid4

from corestore import app
from corestore import corewar
from corestore import database


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/warriors/add", methods=['GET', 'POST'])
def add_warrior():
    # GET request means we have no data, so show the form
    if request.method == 'GET':
        return render_template('new_warrior.html')
    # POST request means we have data, so deal with it
    elif request.method == 'POST':
        (return_code, output, program_data) = corewar.validate(
            request.form.get('source', ""))
        if return_code != 0:
            return render_template('new_warrior_result.html',
                                   success=False,
                                   message=output.replace('\n', '<br />'))
        else:
            # Populate the session with all the relevant information
            session['program_name'] = program_data['name']
            session['program_author'] = program_data['author']
            session['program_source'] = program_data['source']
            session['xss'] = uuid4()
            return render_template('new_warrior_result.html',
                                   success=True,
                                   xss=session['xss'],
                                   message=output.replace('\n', '<br />'))


@app.route("/warriors/commit", methods=["POST"])
def commit_warrior():
    # POST request will have the data we need to insert into the database
    if str(request.form.get('xss', "")) != str(session['xss']):
        return "400 BAD REQUEST: XSS validation failed." +\
            "You may be under attack."\
            .format(request.form.get('xss'), session['xss']), 400

    warrior = database.get_warrior_from_data(session['program_name'],
                                             session['program_author'],
                                             session['program_source'])
    try:
        database.warrior_exists(warrior)
    except database.WarriorExistsWithThatNameException:
        return render_template("error_name_exists.html",
                               name=warrior['name'])
    except database.WarriorExistsWithThatAuthorException:
        return render_template("error_author_exists.html",
                               author=warrior['author'])
    return "ID" + str(database.add_warrior(warrior)), 200


@app.route("/warriors/list")
def list_warriors():
    return render_template("warrior_list.html",
                           programs=database.list_warriors())


@app.route("/warriors/remove")
def remove_warrior():
    return "Not Implemented!", 500
