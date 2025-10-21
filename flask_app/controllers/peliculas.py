from flask import render_template, redirect, request, session, url_for, abort
from .. import app
from ..models.pelicula import Pelicula, Comentario
from ..models.usuario import Usuario


def require_login():
    if "user_id" not in session:
        return redirect("/")
    return None


@app.get("/cine")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    peliculas = Pelicula.obtener_todas()
    usuario = Usuario.obtener_por_id(session["user_id"]) if session.get("user_id") else None
    return render_template("dashboard.html", peliculas=peliculas, usuario=usuario)


@app.get("/cine/nueva")
def nueva_peli():
    need = require_login()
    if need:
        return need
    return render_template("nueva_.html")
 

@app.post("/cine/crear")
def crear_peli():
    need = require_login()
    if need:
        return need
    form = dict(request.form)
    form["usuario_id"] = session["user_id"]
    if not Pelicula.validar(form):
        session["form_peli"] = {k: v for k, v in form.items() if k != "usuario_id"}
        return redirect(url_for("nueva_peli"))
    Pelicula.crear(
        {
            "nombre": form["nombre"].strip(),
            "director": form["director"].strip(),
            "fecha_estreno": form["fecha_estreno"],
            "sinopsis": form["sinopsis"].strip(),
            "usuario_id": session["user_id"],
        }
    )
    session.pop("form_peli", None)
    return redirect(url_for("dashboard"))


@app.get("/cine/editar/<int:peli_id>")
def editar_peli(peli_id: int):
    need = require_login()
    if need:
        return need
    peli = Pelicula.obtener_por_id(peli_id)
    if not peli:
        abort(404)
    return render_template("editar_.html", peli=peli)


@app.post("/cine/actualizar/<int:peli_id>")
def actualizar_peli(peli_id: int):
    need = require_login()
    if need:
        return need
    peli = Pelicula.obtener_por_id(peli_id)
    if not peli:
        abort(404)
    if int(peli["usuario_id"]) != int(session["user_id"]):
        return redirect(url_for("dashboard"))
    form = dict(request.form)
    form["id"] = peli_id
    if not Pelicula.validar(form):
        return redirect(url_for("editar_peli", peli_id=peli_id))
    Pelicula.actualizar(
        {
            "id": peli_id,
            "nombre": form["nombre"].strip(),
            "director": form["director"].strip(),
            "fecha_estreno": form["fecha_estreno"],
            "sinopsis": form["sinopsis"].strip(),
        }
    )
    return redirect(url_for("dashboard"))


@app.get("/cine/borrar/<int:peli_id>")
def borrar_peli(peli_id: int):
    need = require_login()
    if need:
        return need
    peli = Pelicula.obtener_por_id(peli_id)
    if peli and int(peli["usuario_id"]) == int(session["user_id"]):
        Pelicula.borrar(peli_id)
    return redirect(url_for("dashboard"))


@app.get("/cine/<int:peli_id>")
def ver_peli(peli_id: int):
    need = require_login()
    if need:
        return need
    peli = Pelicula.obtener_por_id(peli_id)
    if not peli:
        abort(404)
    comentarios = Comentario.listar_para_pelicula(peli_id)
    return render_template("ver_.html", peli=peli, comentarios=comentarios)


@app.post("/cine/<int:peli_id>/comentar")
def comentar(peli_id: int):
    need = require_login()
    if need:
        return need
    peli = Pelicula.obtener_por_id(peli_id)
    if not peli:
        abort(404)
    if int(peli["usuario_id"]) == int(session["user_id"]):
        return redirect(url_for("ver_peli", peli_id=peli_id))
    contenido = request.form.get("contenido", "").strip()
    if contenido:
        Comentario.crear({
            "contenido": contenido,
            "usuario_id": session["user_id"],
            "pelicula_id": peli_id,
        })
    return redirect(url_for("ver_peli", peli_id=peli_id))


@app.get("/cine/<int:peli_id>/comentarios/<int:comentario_id>/borrar")
def borrar_comentario(peli_id: int, comentario_id: int):
    need = require_login()
    if need:
        return need
    Comentario.borrar_si_propietario(comentario_id, session["user_id"])
    return redirect(url_for("ver_peli", peli_id=peli_id))


