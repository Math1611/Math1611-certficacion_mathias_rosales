from typing import Dict, Any, List, Optional
from flask import flash
from ..config.mysqlconnection import connectToMySQL


DB = "cinepedia_db"


class Pelicula:
    @staticmethod 
    def validar(form: Dict[str, Any]) -> bool:
        es_valido = True
        if len(form.get("nombre", "").strip()) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "pelicula")
            es_valido = False
        if len(form.get("director", "").strip()) < 3:
            flash("El director debe tener al menos 3 caracteres", "pelicula")
            es_valido = False
        if not form.get("fecha_estreno"):
            flash("La Fecha de Estreno es obligatoria", "pelicula")
            es_valido = False
        if len(form.get("sinopsis", "").strip()) == 0:
            flash("Sinopsis no puede estar vacía", "pelicula")
            es_valido = False
        existente = Pelicula.obtener_por_nombre(form.get("nombre", "").strip())
        if existente and (str(existente["id"]) != str(form.get("id", ""))):
            flash("El nombre de la película debe ser único", "pelicula")
            es_valido = False
        return es_valido

    @staticmethod
    def crear(data: Dict[str, Any]) -> int:
        query = (
            "INSERT INTO peliculas (nombre, director, fecha_estreno, sinopsis, usuario_id) "
            "VALUES (%(nombre)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s)"
        )
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def actualizar(data: Dict[str, Any]) -> None:
        query = (
            "UPDATE peliculas SET nombre=%(nombre)s, director=%(director)s, "
            "fecha_estreno=%(fecha_estreno)s, sinopsis=%(sinopsis)s WHERE id=%(id)s"
        )
        connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def borrar(peli_id: int) -> None:
        connectToMySQL(DB).query_db("DELETE FROM comentarios WHERE pelicula_id=%(id)s", {"id": peli_id})
        connectToMySQL(DB).query_db("DELETE FROM peliculas WHERE id=%(id)s", {"id": peli_id})

    @staticmethod
    def obtener_todas() -> List[Dict[str, Any]]:
        query = (
            "SELECT p.*, CONCAT(u.nombre, ' ', u.apellido) AS autor "
            "FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id ORDER BY p.fecha_estreno DESC"
        )
        return connectToMySQL(DB).query_db(query)

    @staticmethod
    def obtener_por_id(peli_id: int) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT p.*, CONCAT(u.nombre, ' ', u.apellido) AS autor, u.id AS autor_id "
            "FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id WHERE p.id=%(id)s"
        )
        res = connectToMySQL(DB).query_db(query, {"id": peli_id})
        return res[0] if res else None

    @staticmethod
    def obtener_por_nombre(nombre: str) -> Optional[Dict[str, Any]]:
        res = connectToMySQL(DB).query_db("SELECT * FROM peliculas WHERE nombre=%(n)s LIMIT 1", {"n": nombre})
        return res[0] if res else None


class Comentario:
    @staticmethod
    def crear(data: Dict[str, Any]) -> int:
        query = "INSERT INTO comentarios (contenido, usuario_id, pelicula_id) VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s)"
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def listar_para_pelicula(peli_id: int) -> List[Dict[str, Any]]:
        query = (
            "SELECT c.*, CONCAT(u.nombre, ' ', u.apellido) AS autor, u.id AS autor_id "
            "FROM comentarios c JOIN usuarios u ON u.id=c.usuario_id "
            "WHERE c.pelicula_id=%(id)s ORDER BY c.created_at DESC"
        )
        return connectToMySQL(DB).query_db(query, {"id": peli_id})

    @staticmethod
    def borrar_si_propietario(comentario_id: int, usuario_id: int) -> None:
        query = "DELETE FROM comentarios WHERE id=%(id)s AND usuario_id=%(uid)s"
        connectToMySQL(DB).query_db(query, {"id": comentario_id, "uid": usuario_id})


