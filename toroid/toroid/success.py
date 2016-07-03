from flask import render_template


def success_page(message, status=200):
    ' Return a rendered status page with the given message. '
    return render_template('success.html',
                           message=message), status
