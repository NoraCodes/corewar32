from flask import render_template


def error_page(error_message, status=200):
    ' Return a rendered error page with the given message. '
    return render_template('error.html',
                           message=error_message), status
