from flask import Blueprint, request, render_template, redirect

from src.services.auth import login_user, AuthError, register_user, logout_user

bp = Blueprint('auth', __name__)



@bp.route("/register", methods=["GET", "POST"])
def register_view():
    template_name = "auth/register.html"
    error = ""

    if request.method == "POST":

        # --------------- Validate user input -------------------
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if not username or not password:
            return render_template(template_name, error="Укажите логин или пароль")
        # ------------------------------------------------------

        # ---------------------- Service -----------------------
        try:
            register_user(username=username, password=password)
            return redirect("/login")
        except AuthError as exc:
            error = str(exc)
        # ------------------------------------------------------

    return render_template(template_name, error=error)


@bp.route('/login', methods=["GET", "POST"])
def login_view():
    template_name = "auth/login.html"
    error = ""

    if request.method == "POST":
        # --------------- Validate user input -------------------
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if not username or not password:
            return render_template(template_name, error="Укажите логин или пароль")
        # ------------------------------------------------------

        # ---------------------- Service -----------------------
        try:
            login_user(username=username, password=password)
            return redirect("/")
        except AuthError as exc:
            error = str(exc)
        # ------------------------------------------------------

    return render_template(template_name, error=error)


@bp.route('/logout', methods=["POST"])
def logout_view():
    logout_user()
    return redirect("/login")
