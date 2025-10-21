from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import re
from flask import flash
from ..config.mysqlconnection import connectToMySQL


DB = "cinepedia_db"

 
@dataclass
class Usuario:
    id: int
    nombre: str
    apellido: str
    email: str
    password_hash: str
    created_at: str
    updated_at: str

    @staticmethod
    def validar_registro(form: Dict[str, Any]) -> bool:
        es_valido = True
        if len(form.get("nombre", "")) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "registro")
            es_valido = False
        if len(form.get("apellido", "")) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "registro")
            es_valido = False
        correo = form.get("email", "").strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            flash("Email inválido", "registro")
            es_valido = False
        existente = Usuario.obtener_por_email(correo)
        if existente:
            flash("El email ya existe en la BD", "registro")
            es_valido = False
        if len(form.get("password", "")) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "registro")
            es_valido = False
        if form.get("password") != form.get("confirmar"):
            flash("Contraseña y confirmación deben ser iguales", "registro")
            es_valido = False
        return es_valido

    @staticmethod
    def validar_login(form: Dict[str, Any]) -> bool:
        correo = form.get("email", "").strip().lower()
        if not Usuario.obtener_por_email(correo):
            flash("El email no está registrado", "login")
            return False
        return True

    @staticmethod
    def crear(data: Dict[str, Any]) -> int:
        query = (
            "INSERT INTO usuarios (nombre, apellido, email, password_hash) "
            "VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s)"
        )
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def obtener_por_email(email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM usuarios WHERE email=%(email)s LIMIT 1"
        resultado = connectToMySQL(DB).query_db(query, {"email": email})
        return resultado[0] if resultado else None

    @staticmethod
    def obtener_por_id(user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM usuarios WHERE id=%(id)s"
        resultado = connectToMySQL(DB).query_db(query, {"id": user_id})
        return resultado[0] if resultado else None


