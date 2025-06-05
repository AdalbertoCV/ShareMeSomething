import os
import uuid
import re
from django.core.exceptions import ValidationError

def generar_nombre_imagen(instance, filename):
    """
    Genera un nombre de archivo único con la extensión original
    """
    extension = os.path.splitext(filename)[1]
    nuevo_nombre = f"{uuid.uuid4().hex}{extension}"
    return os.path.join('usuarios', 'fotos', nuevo_nombre)


def validar_contraseña_segura(value):
    """
    Valida que la contraseña contenga al menos:
    - 8 caracteres
    - 1 mayúscula
    - 1 minúscula
    - 1 número
    - 1 caracter especial
    """
    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", value):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r"\d", value):
        raise ValidationError("La contraseña debe contener al menos un número.")
    if not re.search(r"[^\w\s]", value):
        raise ValidationError("La contraseña debe contener al menos un carácter especial.")