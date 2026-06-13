import secrets
import string
from typing import Optional
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from academico_cursos.models import Curso
from .models import Estudiante

Usuario = get_user_model()


class EstudianteFactory:

    @staticmethod
    def generar_codigo_estudiantil() -> str:
        year = datetime.now().year

        # 5 caracteres: 3 letras + 2 dígitos
        letras = ''.join(
            secrets.choice(string.ascii_uppercase) for _ in range(3)
        )
        digitos = ''.join(
            secrets.choice(string.digits) for _ in range(2)
        )

        codigo = f'EST-{year}-{letras}{digitos}'

        # Validar que sea único
        while Estudiante.objects.filter(
            codigo_estudiantil=codigo
        ).exists():
            letras = ''.join(
                secrets.choice(string.ascii_uppercase) for _ in range(3)
            )
            digitos = ''.join(
                secrets.choice(string.digits) for _ in range(2)
            )
            codigo = f'EST-{year}-{letras}{digitos}'

        return codigo

    @staticmethod
    @transaction.atomic
    def crear(
        *,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        fecha_nacimiento,
        correo_electronico: str,
        curso: Curso,
        telefono: str = '',
        direccion: str = '',
        estado: str = Estudiante.Estado.ACTIVO,
        crear_usuario: bool = False,
        foto=None,
    ) -> Estudiante:

        codigo = EstudianteFactory.generar_codigo_estudiantil()
        usuario_obj = None

        if crear_usuario:
            # Username: primer nombre + número de documento
            base_username = (
                f'{nombres.split()[0].lower()}{numero_documento}'
            )

            username = base_username
            counter = 1

            while Usuario.objects.filter(
                username=username
            ).exists():
                username = f'{base_username}{counter}'
                counter += 1

            usuario_obj = Usuario.objects.create_user(
                username=username,
                email=correo_electronico,
                password=numero_documento,  # contraseña inicial
                first_name=nombres,
                last_name=apellidos,
            )

            usuario_obj.rol = Usuario.Rol.ESTUDIANTE
            usuario_obj.telefono = telefono
            usuario_obj.save()

        return Estudiante.objects.create(
            codigo_estudiantil=codigo,
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            fecha_nacimiento=fecha_nacimiento,
            correo_electronico=correo_electronico,
            telefono=telefono,
            direccion=direccion,
            estado=estado,
            curso=curso,
            usuario=usuario_obj,
            foto=foto,
        )


estudiante_factory = EstudianteFactory()