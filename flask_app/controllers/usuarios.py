from flask import render_template, redirect, request, session, url_for
from .. import app, bcrypt
from ..models.usuario import Usuario


@app.get("/")
def index():
    return render_template("index.html")
 

@app.post("/registrar")
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect("/")
    password_hash = bcrypt.generate_password_hash(request.form["password"]).decode()
    user_id = Usuario.crear(
        {
            "nombre": request.form["nombre"].strip(),
            "apellido": request.form["apellido"].strip(),
            "email": request.form["email"].strip().lower(),
            "password_hash": password_hash,
        }
    )
    session["user_id"] = int(user_id)
    return redirect(url_for("dashboard"))


@app.post("/login")
def login():
    if not Usuario.validar_login(request.form):
        return redirect("/")
    user = Usuario.obtener_por_email(request.form["email"].strip().lower())
    if not bcrypt.check_password_hash(user["password_hash"], request.form["password"]):
        from flask import flash

        flash("Contraseña incorrecta", "login")
        return redirect("/")
    session["user_id"] = int(user["id"])
    return redirect(url_for("dashboard"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")


