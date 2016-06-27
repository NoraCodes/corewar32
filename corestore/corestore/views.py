from flask import request, render_template
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
        (return_code, output, program_data) = corewar.validate(request.form.get('source', ""))
        if return_code != 0:
            return render_template('new_warrior_result.html',
                                    success=False,
                                    message=output.replace('\n', '<br />'))
        else:
            return render_template('new_warrior_result.html',
                                    success=True,
                                    name=program_data['name'],
                                    author=program_data['author'],
                                    source=program_data['source'],
                                    message=output.replace('\n', '<br />'))

@app.route("/warriors/commit", methods=["POST"])
def commit_warrior():
    # POST request will have the data we need to insert into the database
    warrior = { 'name': request.form.get('name', ""),
                'author': request.form.get('author', ""),
                'source': request.form.get('source', "")}
    return str(database.add_warrior(warrior))

@app.route("/warriors/list")
def list_warriors():
    return "Not Implemented!", 500


@app.route("/warriors/remove")
def remove_warrior():
    return "Not Implemented!", 500
