import functools
from flask import redirect, url_for, request, session


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "name" not in session:
            return redirect(url_for("login.login", next=request.url))
        return func(*args, **kwargs)

    return secure_function
