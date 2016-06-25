from flask import request, render_template
from corestore import app
from corestore import corewar


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/warriors/add", methods=['GET', 'POST'])
def add_warrior():
    if request.method == 'GET':
        return render_template('new_warrior.html')
    elif request.method == 'POST':
        (ret, out) = corewar.validate(request.form.get('source', None))
        if ret != 0:
            return render_template('new_warrior_result.html',
                                    success=False,
                                    message=out.replace('\n', '<br />'))
        else:
            return render_template('new_warrior_result.html',
                                    success=True,
                                    message=out.replace('\n', '<br />'))

@app.route("/warriors/list")
def list_warriors():
    return "Not Implemented!", 500


@app.route("/warriors/remove")
def remove_warrior():
    return "Not Implemented!", 500
