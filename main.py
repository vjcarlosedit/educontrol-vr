import flet as ft
from datetime import datetime, timedelta
from supabase import create_client, Client

SUPABASE_URL = "https://doyjqcrxglfopgggmdus.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRveWpxY3J4Z2xmb3BnZ2dtZHVzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMzE4Mzg2MCwiZXhwIjoyMDQ4NzU5ODYwfQ.F0QX4UXpg2UycmrS1beQ5edr7yoaepjuVfx5Z8GJpYc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para redirigir a la página de inicio
def navigate_to_home(page):
    pass

# Página de inicio de sesión
def login_screen(page):
    
    def navigate_to_register(e):
        register_screen(page)

    def custom_button():
        return ft.Container(
            content=ft.Text(
                "Acceder",
                size=16,
                color="white",
                weight="bold",
                text_align="center",
                font_family="MontserratBold",
            ),
            bgcolor="#4CAF50",
            border_radius=10,
            alignment=ft.alignment.center,
            padding=ft.Padding(10, 10, 10, 10),
            width=300,
            on_click=handle_login,  # Aquí se conecta el botón con la lógica de login
        )

    # Función para manejar el login
    def handle_login(e):
        correo = str(correo_electronico.value)  # Correo del usuario
        password = str(contrasena.value)  # Contraseña del usuario

        # Validaciones dinámicas
        if not correo.strip():
            mensaje_validacion.value = "El campo 'Correo electrónico' es obligatorio."
            page.update()
        elif "@" not in correo or (not correo.endswith(".com") and not correo.endswith(".mx")):
            mensaje_validacion.value = "Ingrese un correo electrónico válido."
            page.update()
        elif not password.strip():
            mensaje_validacion.value = "El campo 'Contraseña' es obligatorio."
            page.update()
        else:
            # Verificar si el correo existe en la base de datos
            response = supabase.table("usuario").select("*").eq("correo_electronico", correo).execute()

            if response.data:
                usuario_db = response.data[0]  # Obtener el primer usuario encontrado
                if usuario_db["contrasena"] == password:  # Comparar las contraseñas
                    mensaje_validacion.value = "¡Inicio de sesión exitoso!"
                    mensaje_validacion.color = "green"  # Cambia el color si es exitoso
                    print("Acceso concedido para:", correo)

                    # Verificar si los campos requeridos están vacíos
                    if not usuario_db["division_academica"] or not usuario_db["licenciatura"] or not usuario_db["asignatura_grupo"]:
                        # Si alguno de los campos está vacío, redirigir al usuario a editar perfil
                        print("Por favor, complete su perfil.")
                        edit_profile(page, correo)
                    else:
                        # Si los campos están completos, continuar a la página principal
                        print("Inicio Sesion Correcto") # O cualquier otra página de inicio
                        home(page, correo)

                else:
                    mensaje_validacion.value = "Contraseña incorrecta."
                    page.update()
            else:
                mensaje_validacion.value = "Correo electrónico no registrado."
                page.update()

            page.update()  # Actualiza la página para mostrar el mensaje de validación
    # Variables de entrada para correo y contraseña
    correo_electronico = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.icons.PERSON,
        width=300,
    )

    contrasena = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300,
    )

    # Texto dinámico para las validaciones
    mensaje_validacion = ft.Text(
        "",
        size=12,
        color="red",
        weight="bold",
        text_align="center",
    )

    # Contenido de la columna para la interfaz de login
    column = ft.Column(
        [
            ft.Text(
                "INICIAR SESIÓN",
                style="headlineSmall",
                text_align="center",
                size=20,
                font_family="MontserratBold",
            ),
            correo_electronico,
            contrasena,
            mensaje_validacion,  # Aquí se agregará el mensaje de validación
            custom_button(),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "¿No tienes cuenta?",
                            size=12,
                            weight="normal",
                            color="black",
                        ),
                        ft.Container(
                            content=ft.Text(
                                " Regístrate aquí.",
                                size=12,
                                color="blue",
                                weight="bold",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,
                                ),
                            ),
                            on_click=navigate_to_register,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    container_with_background = ft.Container(
        content=column,
        width=400,
        height=450,
        bgcolor="#F2F2F2",
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )

    footer = ft.Container(
        content=ft.Text(
            "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
            "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
            size=12,
            color="white",
            text_align="center",
        ),
        bgcolor="#333333",
        padding=10,
        alignment=ft.alignment.center,
        expand=False,
    )

    main_container = ft.Container(
        content=container_with_background,
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
    )

    page.clean()
    page.add(
        ft.Column(
            [
                main_container,
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )
    page.update()
    
# Página de registro
def register_screen(page):

    # Variables para almacenar los TextFields
    nombre_completo = ft.TextField(
        label="Nombre completo",
        prefix_icon=ft.icons.PERSON,
        width=300,
    )

    correo_electronico = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.icons.EMAIL,
        width=300,
    )

    contrasena = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300,
    )

    confirmar_contrasena = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300,
    )

    # Texto dinámico para las validaciones
    mensaje_validacion = ft.Text(
        "",
        size=12,
        color="red",
        weight="bold",
        text_align="center",
    )

    # Función para manejar el registro
    def handle_register(e):
        nombre = str(nombre_completo.value)
        correo = str(correo_electronico.value)
        password = str(contrasena.value)
        confirm_password = str(confirmar_contrasena.value)

        # Validaciones dinámicas
        if not nombre.strip():
            mensaje_validacion.value = "El campo 'Nombre completo' es obligatorio."
            page.update()
        elif not correo.strip():
            mensaje_validacion.value = "El campo 'Correo electrónico' es obligatorio."
            page.update()
        elif "@" not in correo or (not correo.endswith(".com") and not correo.endswith(".mx")):
            mensaje_validacion.value = "Ingrese un correo electrónico válido."
            page.update()
        elif not password.strip():
            mensaje_validacion.value = "El campo 'Contraseña' es obligatorio."
            page.update()
        elif len(password) < 6:
            mensaje_validacion.value = "La contraseña debe tener al menos 6 caracteres."
            page.update()
        elif password != confirm_password:
            mensaje_validacion.value = "Las contraseñas no coinciden."
            page.update()
        else:
            # Verificar si el correo ya está registrado
            response = supabase.table("usuario").select("*").eq("correo_electronico", correo).execute()
            
            if response.data:
                mensaje_validacion.value = "El correo electrónico ya está registrado."
            else:
                mensaje_validacion.value = "¡Registro exitoso!"
                mensaje_validacion.color = "green"  # Cambia el color si es exitoso
                page.update()
                # Aquí puedes añadir lógica para guardar los datos del usuario
                print(f"Nombre: {nombre}, Correo: {correo}, Contraseña: {password}")

                usuario = {
                    "nombre_completo": nombre,
                    "correo_electronico": correo,
                    "contrasena": password,
                    "division_academica": None,
                    "licenciatura": None,
                    "asignatura_grupo": None,
                }

                # Insertar el usuario en la base de datos
                insert_response = supabase.table("usuario").insert(usuario).execute()

                if insert_response.data:
                    print("Usuario agregado correctamente:", insert_response.data)
                elif insert_response.error:
                    print("Error al agregar usuario:", insert_response.error)

            page.update()


    # Función para cambiar a la pantalla de login
    def navigate_to_login(e):
        login_screen(page)

    def custom_button():
        return ft.Container(
            content=ft.Text(
                "Registrarse",
                size=16,
                color="white",
                weight="bold",
                text_align="center",
                font_family="MontserratBold",
            ),
            bgcolor="#4CAF50",
            border_radius=10,
            alignment=ft.alignment.center,
            padding=ft.Padding(10, 10, 10, 10),
            width=300,
            on_click=handle_register,
        )

    column = ft.Column(
        [
            ft.Text(
                "REGISTRARSE",
                style="headlineSmall",
                text_align="center",
                size=20,
                font_family="MontserratBold",
            ),
            nombre_completo,
            correo_electronico,
            contrasena,
            confirmar_contrasena,
            mensaje_validacion,  # Agregamos el texto de validación aquí
            custom_button(),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "¿Ya estás registrado?",
                            size=12,
                            weight="normal",
                            color="black",
                        ),
                        ft.Container(
                            content=ft.Text(
                                " Inicia sesión aquí.",
                                size=12,
                                color="blue",
                                weight="bold",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,
                                ),
                            ),
                            on_click=navigate_to_login,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    container_with_background = ft.Container(
        content=column,
        width=400,
        height=500,
        bgcolor="#F2F2F2",
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )

    footer = ft.Container(
        content=ft.Text(
            "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
            "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
            size=12,
            color="white",
            text_align="center",
            font_family="MontserratBold",
        ),
        bgcolor="#333333",
        padding=10,
        alignment=ft.alignment.center,
        expand=False,
    )

    main_container = ft.Container(
        content=container_with_background,
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
    )

    page.clean()
    page.add(
        ft.Column(
            [
                main_container,
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )
    page.update()

# Pantalla para editar el perfil
def edit_profile(page, correo):

    # print(correo)
    correo_value = correo
    response = supabase.table("usuario").select("*").eq("correo_electronico", correo_value).execute()
    if response.data:
            usuario = response.data[0]
            nombre_completo = usuario.get("nombre_completo", "")
            correo_electronico = usuario.get("correo_electronico", "")
            contrasena = usuario.get("contrasena", "")
            division_academica = usuario.get("division_academica", "")
            licenciatura = usuario.get("licenciatura", "")
            asignatura_grupo = usuario.get("asignatura_grupo", "")

            # # Puedes hacer lo que necesites con los datos, por ejemplo, mostrarlos en la página
            # print(f"Nombre Completo: {nombre_completo}")
            # print(f"Correo Electrónico: {correo_electronico}")
            # print(f"Contraseña: {contrasena}")
            # print(f"División Académica: {division_academica}")
            # print(f"Licenciatura: {licenciatura}")
            # print(f"Asignatura - Grupo: {asignatura_grupo}")

    nombre_completo = ft.TextField(
        label="Nombre Completo",
        prefix_icon=ft.icons.PERSON,
        width=300,
        value=nombre_completo,
    )
    
    correo_electronico = ft.TextField(
        label="Correo Electrónico",
        prefix_icon=ft.icons.EMAIL,
        width=300,
        filled=True,
        value=correo_value,  # Este es el valor que deseas mostrar
        read_only=True,  # Esto hace que el campo no sea modificable
    )

    division_academica = ft.TextField(
        label="División Académica",
        width=300,
        # value=division_academica_value,
    )

    licenciatura = ft.TextField(
        label="Licenciatura",
        width=300,
        # value=licenciatura_value,
    )

    asignatura_grupo = ft.TextField(
        label="Asignatura - Grupo",
        width=300,
        # value=asignatura_value,
    )

    # # Texto dinámico para las validaciones
    mensaje_validacion = ft.Text(
        "",
        size=12,
        color="red",
        weight="bold",
        text_align="center",
    )

    # Función para manejar la actualización del perfil
    def handle_update_profile(e):

        nombre = str(nombre_completo.value)
        correo = str(correo_electronico.value)
        division = str(division_academica.value)
        licenciatura_value = str(licenciatura.value)
        asignatura = str(asignatura_grupo.value)

        # Validaciones dinámicas
        if not nombre.strip():
            mensaje_validacion.value = "El campo 'Nombre completo' es obligatorio."
            page.update()
        elif not division.strip():
            mensaje_validacion.value = "El campo 'División Académica' es obligatorio."
            page.update()
        elif not licenciatura_value.strip():
            mensaje_validacion.value = "El campo 'Licenciatura' es obligatorio."
            page.update()
        elif not asignatura.strip():
            mensaje_validacion.value = "El campo 'Asignatura' es obligatorio."
            page.update()
        else:
            # Actualizar los datos del usuario en la base de datos
            usuario = {
                "nombre_completo": nombre,
                "correo_electronico": correo,
                "division_academica": division,
                "licenciatura": licenciatura_value,
                "asignatura_grupo": asignatura,
            }
            # Actualizar los datos en la base de datos
            update_response = supabase.table("usuario").update(usuario).eq("correo_electronico", correo_value).execute()

            if update_response.data:
                mensaje_validacion.color = "green"  # Cambia el color si es exitoso
                mensaje_validacion.value = "Perfil actualizado con éxito."
                
                home(page, correo)
            else:
                mensaje_validacion.value = "Error al actualizar el perfil."
            
            page.update()

    # Contenedor para los botones
    def custom_button():
        return ft.Container(
            content=ft.Text(
                "Guardar",
                size=16,
                color="white",
                weight="bold",
                text_align="center",
                font_family="MontserratBold",
            ),
            bgcolor="#4CAF50",
            border_radius=10,
            alignment=ft.alignment.center,
            padding=ft.Padding(10, 10, 10, 10),
            width=300,
            on_click=handle_update_profile,
        )


    # Contenedor con los campos de texto
    column = ft.Column(
        [
            ft.Text(
                "EDITAR PERFIL",
                style="headlineSmall",
                text_align="center",
                size=20,
                font_family="MontserratBold",
            ),
            nombre_completo,
            correo_electronico,
            division_academica,
            licenciatura,
            asignatura_grupo,
            mensaje_validacion,  # Agregamos el texto de validación aquí
            custom_button(),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "¿Deseas salir?",
                            size=12,
                            weight="normal",
                            color="black",
                        ),
                        ft.Container(
                            content=ft.Text(
                                " Regresa a inicio.",
                                size=12,
                                color="blue",
                                weight="bold",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,
                                ),
                            ),
                            on_click=lambda e: main(page),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    container_with_background = ft.Container(
        content=column,
        width=400,
        height=500,
        bgcolor="#F2F2F2",
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )

    footer = ft.Container(
        content=ft.Text(
            "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
            "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
            size=12,
            color="white",
            text_align="center",
            font_family="MontserratBold",
        ),
        bgcolor="#333333",
        padding=10,
        alignment=ft.alignment.center,
        expand=False,
    )

    main_container = ft.Container(
        content=container_with_background,
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
    )

    page.clean()
    page.add(
        ft.Column(
            [
                main_container,
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )
    page.update()

# Página principal
def home(page, correo):

    # PAGINA RESERVACIÓN


    def actualizar_fecha(e):
            global fecha_seleccionada
            fecha_seleccionada = e.control.value
            print(f"Fecha seleccionada: {fecha_seleccionada}")
            page.update()

    def actualizar_hora(e):
            global hora_seleccionada
            hora_seleccionada = e.control.value
            print(f"Hora seleccionada: {hora_seleccionada}")
            page.update()

    def reset_dropdowns():
        # Vaciar los campos agregando una opción predeterminada
        txt_fecha.options = [ft.dropdown.Option("", "Seleccione una fecha")] + txt_fecha.options[1:]
        txt_hora.options = [ft.dropdown.Option("", "Seleccione una hora")] + txt_hora.options[1:]
        
        # Actualizar la UI
        page.update()

    def handle_reservacion(e):

        # if not fecha_seleccionada:
        #     mensaje_validacion.value = "Error: Selecciona una fecha válida."
        #     mensaje_validacion.color = "red"
        #     page.update()  # Actualiza la UI inmediatamente
        #     return


        # if not hora_seleccionada:
        #     mensaje_validacion.value = "Error: Selecciona una hora válida."
        #     mensaje_validacion.color = "red"
        #     page.update()
        #     return

        if not txt_asignatura.value.strip():
            mensaje_validacion_equipo.value = "Error: El grupo no puede estar vacío."
            mensaje_validacion_equipo.color = "red"
            page.update()
            return
        
        if not txt_estudiantes.value.isdigit():
            mensaje_validacion_equipo.value = "Error: El número de estudiantes debe ser un número."
            mensaje_validacion_equipo.color = "red"
            page.update()
            return        

        global fecha_seleccionada, hora_seleccionada
        print(f"Procesando reservación con Fecha: {fecha_seleccionada}, Hora: {hora_seleccionada}")

        correo_usuario = correo
        response = supabase.from_("usuario").select("id_usuario").eq("correo_electronico", correo_usuario).execute()
        
        if response.data:
            id_usuario = response.data[0]['id_usuario']
            print(f"ID del usuario: {id_usuario}")
        else:
            print("Usuario no encontrado.") 


        division = str(txt_division.value.strip())
        licenciatura = str(txt_licenciatura.value.strip())
        asignatura = str(txt_asignatura.value.strip())
        numero_estudiantes = str(txt_estudiantes.value.strip())

        datos_reservacion = {
                "division_academica": division,
                "licenciatura": licenciatura,
                "asignatura": asignatura,
                "numero_estudiantes": numero_estudiantes,
                "fecha": fecha_seleccionada,
                "hora": hora_seleccionada,
                "id_usuario": id_usuario  # Reemplaza con un id_usuario válido
        }

        try:
            response = supabase.table("reservacion").insert(datos_reservacion).execute()
            # print("Datos insertados:", response.data)
            
            # Mensaje de registro exitoso mejorado
            mensaje_vali.value = "Reservación exitosa."
            mensaje_vali.color = "green"

            # Vaciar los campos
            txt_division.value = None  # Vaciar selección
            txt_licenciatura.value = None
            txt_asignatura.value = ""
            txt_estudiantes.value = ""
            page.update()
            
        except Exception as e:
            print("Error al insertar los datos:", e)
            mensaje_vali.value = "Error al realizar la reservación."
            mensaje_vali.color = "red"
            page.update()

    def actualizar_licenciaturas(e):
            # Obtén la selección actual del Dropdown de División Académica
            seleccion_division = txt_division.value
            # Actualiza las opciones del Dropdown de Licenciatura
            txt_licenciatura.options = [
                ft.dropdown.Option(lic) for lic in divisiones_licenciaturas[seleccion_division]
            ]
            # Establece el valor predeterminado en la primera licenciatura
            txt_licenciatura.value = divisiones_licenciaturas[seleccion_division][0]
            # Refresca el Dropdown en la UI
            page.update()

        # Vincula la función al cambio de selección del Dropdown de División Académica
            txt_division.on_change = actualizar_licenciaturas
    
    divisiones_licenciaturas = {
    "DACA": [
        "Ingeniería en Acuacultura",
        "Ingeniería en Agronomía",
        "Ingeniería en Alimentos",
        "Medicina Veterinaria y Zootecnia"
    ],
    "DACB": [
        "Ingeniería Geofísica",
        "Licenciatura en Ciencias Computacionales",
        "Licenciatura en Física",
        "Licenciatura en Matemáticas",
        "Licenciatura en Química",
        "Licenciatura en Actuaría",
        "Químico Farmacéutico Biólogo"
    ],
    "DACBiol": [
        "Licenciatura en Biología",
        "Licenciatura en Gestión Ambiental",
        "Licenciatura en Ingeniería Ambiental"
    ],
    "DACEA": [
        "Licenciatura en Administración",
        "Licenciatura en Contaduría Pública",
        "Licenciatura en Economía",
        "Licenciatura en Mercadotecnia"
    ],
    "DACS": [
        "Licenciatura en Médico Cirujano",
        "Licenciatura en Cirujano Dentista",
        "Licenciatura en Psicología",
        "Licenciatura en Nutrición",
        "Licenciatura en Enfermería",
        "Licenciatura en Trabajo Social"
    ],
    "DACSyH": [
        "Licenciatura en Derecho",
        "Licenciatura en Historia",
        "Licenciatura en Sociología",
        "Licenciatura en Gestión y Promoción de la Cultura"
    ],
    "DAEA": [
        "Licenciatura en Ciencias de la Educación",
        "Licenciatura en Comunicación",
        "Licenciatura en Desarrollo Cultural (sistema abierto)",
        "Licenciatura en Idiomas"
    ],
    "DAIA": [
        "Ingeniería Civil",
        "Ingeniería Eléctrica y Electrónica",
        "Ingeniería Mecánica Eléctrica",
        "Ingeniería Química",
        "Licenciatura en Arquitectura"
    ],
    "DAIS": [
        "Licenciatura en Informática Administrativa",
        "Licenciatura en Sistemas Computacionales",
        "Licenciatura en Telemática",
        "Licenciatura en Tecnologías de la Información"
    ],
    "DAMC": [
        "Ingeniería en Acuacultura",
        "Licenciatura en Administración",
        "Ingeniería en Alimentos",
        "Licenciatura en Informática Administrativa"
    ],
    "DAMJ": [
        "Licenciatura en Derecho",
        "Licenciatura en Enfermería"
    ],
    "DAMR": [
        "Licenciatura en Administración",
        "Licenciatura en Enfermería",
        "Licenciatura en Médico Cirujano",
        "Licenciatura en Atención Prehospitalaria y Desastre",
        "Licenciatura en Rehabilitación Física",
        "Licenciatura en Genómica",
        "Licenciatura en Ingeniería Petroquímica",
        "Licenciatura en Ingeniería en Nanotecnología"
    ],
    "DACYTI": [
        "Ingeniería en Informática Administrativa",
        "Ingeniería en Sistemas Computacionales"
    ],
}
    # Componentes de reservación
    titulo_reservacion = ft.Text("NUEVA RESERVACIÓN", style="headlineSmall", color="#4BAF4F", size=20, weight="bold")
    
    
    txt_division = ft.Dropdown(
        label="División Académica",
        options=[ft.dropdown.Option(div) for div in divisiones_licenciaturas.keys()],
        value="DACS",  # Valor predeterminado
        width=300,


        
    )
    txt_licenciatura = ft.Dropdown(
        label="Licenciatura",
        options=[ft.dropdown.Option(lic) for lic in divisiones_licenciaturas["DACS"]],
        value=divisiones_licenciaturas["DACS"][0],  # Primera licenciatura por defecto
        width=300,
    )
    
    txt_asignatura = ft.TextField(label="Grupo", width=300)
    
    
    txt_estudiantes = ft.TextField(label="Número de Estudiantes", width=300)


    def obtener_fechas_laborables():
        # Obtener la fecha de hoy
        hoy = datetime.now()
        fechas = []
        contador = 0

        # Generar las fechas laborables hasta el viernes
        while len(fechas) < 5:
            dia = hoy + timedelta(days=contador)
            # Si es un día laborable (lunes a viernes), lo incluimos
            if dia.weekday() < 5:  # 0=Lunes, 4=Viernes
                fechas.append(dia.strftime("%d-%m-%Y"))
            contador += 1  # Avanzar al siguiente día

        return fechas

    opciones_fechas = obtener_fechas_laborables()

    txt_fecha = ft.Dropdown(
        label="Fecha",
        options=[ft.dropdown.Option(fecha) for fecha in opciones_fechas],
        value=None,  # Primera fecha predeterminada
        width=300,
        on_change=lambda e: actualizar_fecha(e)
    )

    # print("Opciones de fechas:", opciones_fechas)


    opciones_horas = [
        f"{hora:02d}:00" for hora in range(8, 19, 2)  # Rango de 8 a 18 con pasos de 2
    ]
    
    txt_hora = ft.Dropdown(
        label="Hora",
        options=[ft.dropdown.Option(hora) for hora in opciones_horas],
        value=None,  # Hora predeterminada
        width=300,
        on_change=lambda e: actualizar_hora(e)
    )

    
    # print("Opciones de horas:", opciones_horas)
    mensaje_vali = ft.Text(value="", size=12, color="red")

    buttons_row = ft.Row(
        [
            ft.Container(
                content=ft.Text("Cancelar", size=16, color="white"),
                bgcolor="grey",
                border_radius=10,
                alignment=ft.alignment.center,
                padding=ft.Padding(10, 10, 10, 10),
                width=140,
                on_click=lambda e: print("Cancelar"),
            ),
            ft.Container(
                content=ft.Text("Reservar", size=16, color="white"),
                bgcolor="#4CAF50",
                border_radius=10,
                alignment=ft.alignment.center,
                padding=ft.Padding(10, 10, 10, 10),
                width=140,
                on_click=handle_reservacion,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    reservacion_column = ft.Column(
        [
            titulo_reservacion,
            txt_division,
            txt_licenciatura,
            txt_asignatura,
            txt_estudiantes,
            txt_fecha,
            txt_hora,
            mensaje_vali,
            buttons_row,
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centra el contenido verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido horizontalmente
        spacing=15,  # Espaciado entre elementos
        expand=True,  # Permite que la columna ocupe todo el espacio disponible
    )
    page.update()

    # PAGINA PRINCIPAL

    logo_ujat = ft.Image(
    src="https://raw.githubusercontent.com/vjcarlosedit/flet_page/main/assets/logo-ujat.png",
    width=250)

    filaLogo = ft.Row([logo_ujat], alignment="center")

    txtBienvenido = ft.Text(
    "¡Bienvenido!", 
    size=28, 
    text_align="center", 
    color="green"
    )

    txtDatos = ft.Text(
        "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, Vhsa, Centro, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00",
        size=14, 
        text_align="center", 
        color="green",
    )

    principal_colum = ft.Column(
        [txtBienvenido, 
         filaLogo, 
         txtDatos],
        # alignment="center",
        alignment=ft.MainAxisAlignment.CENTER,  # Centra el contenido verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido horizontalmente
        spacing=50
    )
    page.update()

    # PAGINA TABLA RESERVACIÓN  


    def obtener_reservaciones_por_usuario(correo):
        # Paso 1: Obtener el id_usuario a partir del correo electrónico
        response = supabase.from_("usuario").select("id_usuario").eq("correo_electronico", correo).execute()
        reservaciones = []
        
        if response.data:
            id_usuario = response.data[0]['id_usuario']
            
            # Paso 2: Obtener reservaciones asociadas a ese id_usuario
            reservaciones_response = supabase.from_("reservacion").select(
                "fecha, hora, asignatura, division_academica, licenciatura, numero_estudiantes, estado"
            ).eq("id_usuario", id_usuario).execute()
            
            if reservaciones_response.data:
                reservaciones = reservaciones_response.data
            else:
                print("No se encontraron reservaciones para este usuario.")
        else:
            print("Usuario no encontrado.")
        
        return reservaciones
    
    
    correo_usuario = correo
    response = supabase.from_("usuario").select("id_usuario").eq("correo_electronico", correo_usuario).execute()
    
    if response.data:
        id_usuario = response.data[0]['id_usuario']
        print(f"ID del usuario: {id_usuario}")
    else:
        print("Usuario no encontrado.")   

    datos_reservaciones = obtener_reservaciones_por_usuario(correo_usuario)

    # Generar las filas para la tabla
    titulo_mis_reservaciones = ft.Text("MIS RESERVACIONES", style="headlineSmall", color="#4BAF4F", size=20, weight="bold")
    
    

    lista_tabla = []
    for reservacion in datos_reservaciones:
        celda1 = ft.DataCell(ft.Text(reservacion["fecha"]))
        celda2 = ft.DataCell(ft.Text(reservacion["hora"]))
        celda3 = ft.DataCell(ft.Text(reservacion["asignatura"]))
        celda4 = ft.DataCell(ft.Text(reservacion["division_academica"]))
        celda5 = ft.DataCell(ft.Text(reservacion["licenciatura"]))
        celda6 = ft.DataCell(ft.Text(str(reservacion["numero_estudiantes"])))
        celda7 = ft.DataCell(ft.Text(reservacion["estado"]))
        fila = ft.DataRow(cells=[celda1, celda2, celda3, celda4, celda5, celda6, celda7])
        lista_tabla.append(fila)

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Hora")),
        ft.DataColumn(ft.Text("Grupo")),
        ft.DataColumn(ft.Text("División Académica")),
        ft.DataColumn(ft.Text("Licenciatura")),
        ft.DataColumn(ft.Text("N° Estudiantes")),
        ft.DataColumn(ft.Text("Estado")),
    ]

    # Crear la tabla
    tblReservaciones = ft.DataTable(
        columns=encabezado,
        rows=lista_tabla,
    )

    # Contenedor para la tabla
    contenedorTabla = ft.ListView(
        controls=[tblReservaciones],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )

    fecha_actual = datetime.now().strftime("%d-%m-%Y")
    hora_actual = datetime.now().strftime("%H:%M")

    # PAGINA REPORTE



    def handle_enviar(e):
        # Validar campos obligatorios
        if not txt_etiqueta.value:
            mensaje_validacion_equipo.value = "Por favor selecciona una etiqueta."
            mensaje_validacion_equipo.update()
            return

        if not txt_descripcion.value.strip():
            mensaje_validacion_equipo.value = "Por favor ingresa una descripción."
            mensaje_validacion_equipo.update()
            return

        # print(id_usuario)
        # print(txt_etiqueta.value)
        # print(txt_equipo.value)
        # print(txt_categoria.value)
        # print(txt_fecha.value)
        # print(txt_hora.value)
        # print(txt_descripcion.value.strip())

        # Datos a enviar a Supabase
        nuevo_reporte = {
            "etiqueta": str(txt_etiqueta.value),
            "equipo": str(txt_equipo.value),
            "categoria": str(txt_categoria.value),
            "fecha": str(txt_fecha.value),
            "hora": str(txt_hora.value),
            "descripcion": str(txt_descripcion.value.strip()),
            "id_usuario": id_usuario,
        }

        # Insertar el reporte en la tabla "reportes"
        try:
            response = supabase.table("reportes").insert(nuevo_reporte).execute()

            mensaje_validacion_equipo.value = "Reporte enviado correctamente."
            mensaje_validacion_equipo.color = "green"
            # Limpiar campos después de enviar
            txt_etiqueta.value = None
            txt_equipo.value = ""
            txt_categoria.value = ""
            txt_descripcion.value = ""
            txt_etiqueta.update()
            txt_equipo.update()
            txt_categoria.update()
            txt_descripcion.update()
            page.update()
        except Exception as ex:
            mensaje_validacion_equipo.value = f"Error inesperado: {str(ex)}"
            mensaje_validacion_equipo.color = "red"

        mensaje_validacion_equipo.update()
        page.update()


    titulo_reporte = ft.Text("NUEVO REPORTE", style="headlineSmall", color="#4BAF4F", size=20, weight="bold")


    response = supabase.table("equipos").select("nombre, etiqueta, categoria").execute()
    data = response.data  # Datos obtenidos de la tabla

    # Definición de función para actualizar campos
    def actualizar_campos(e, txt_equipo, txt_categoria):
        etiqueta_seleccionada = e.control.value
        for item in data:
            if item["etiqueta"] == etiqueta_seleccionada:
                txt_equipo.value = item["equipo"]
                txt_categoria.value = item["categoria"]
                txt_equipo.update()
                txt_categoria.update()
                break

    txt_etiqueta = ft.Dropdown(
        label="Etiqueta",
        width=300,
        options=[
            ft.dropdown.Option(item["etiqueta"]) for item in data
        ],
        on_change=lambda e: actualizar_campos(e, txt_equipo, txt_categoria),
    )

    txt_categoria = ft.TextField(label="Categoría", width=300)

    txt_equipo =ft.TextField(label="Equipo", width=300)



    txt_fecha = ft.TextField(label=f"Fecha", width=300, value=fecha_actual, read_only=True, filled=True, )
    txt_hora = ft.TextField(label=f"Hora", width=300, value=hora_actual, read_only=True, filled=True,)
    txt_descripcion = ft.TextField(label="Descripción", width=300)
    txt_evidencia = ft.TextField(label="Evidencia", width=300)
    mensaje_validacion_equipo = ft.Text(value="", size=12, color="red")


    buttons_row = ft.Row(
            [
                ft.Container(
                    content=ft.Text("Cancelar", size=16, color="white"),
                    bgcolor="grey",
                    border_radius=10,
                    alignment=ft.alignment.center,
                    padding=ft.Padding(10, 10, 10, 10),
                    width=140,
                    on_click=lambda e: print("Cancelar"),
                ),
                ft.Container(
                    content=ft.Text("Enviar", size=16, color="white"),
                    bgcolor="#4CAF50",
                    border_radius=10,
                    alignment=ft.alignment.center,
                    padding=ft.Padding(10, 10, 10, 10),
                    width=140,
                    on_click=handle_enviar,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    gestion_column = ft.Column(

                [
                    titulo_reporte,
                    txt_etiqueta,
                    txt_equipo,
                    txt_categoria,
                    txt_fecha,
                    txt_hora,
                    txt_descripcion,
                    # txt_evidencia,
                    mensaje_validacion_equipo,
                    buttons_row,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centra el contenido verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido horizontalmente
                spacing=15,  # Espaciado entre elementos
                expand=True,  # Permite que la columna ocupe todo el espacio disponible
            )
    
    # PAGINA TABLA GESTIÓN


    response = supabase.table("reportes").select(
        "etiqueta, equipo, categoria, fecha, hora, descripcion, encargado, estado").execute()
    data = response.data  # Datos obtenidos de la tabla77
    # print(data)

    def obtener_reportes_por_usuario(correo):
        # Paso 1: Obtener el id_usuario a partir del correo electrónico
        response = supabase.table("usuario").select("id_usuario").eq("correo_electronico", correo).execute()
        reportes = []

        if response.data:
            id_usuario = response.data[0]["id_usuario"]

            # Paso 2: Obtener reportes asociados a ese id_usuario
            reportes_response = supabase.table("reportes").select(
                "etiqueta, equipo, categoria, fecha, hora, descripcion, encargado, estado"
            ).eq("id_usuario", id_usuario).execute()

            if reportes_response.data:
                reportes = reportes_response.data
            else:
                print("No se encontraron reportes para este usuario.")
        else:
            print("Usuario no encontrado.")

        return reportes
    

    # Obtener los reportes para el usuario
    datos_reportes = obtener_reportes_por_usuario(correo_usuario)

    # Generar las filas para la tabla
    lista_tabla = []
    for reporte in datos_reportes:
        celda1 = ft.DataCell(ft.Text(reporte["etiqueta"]))
        celda2 = ft.DataCell(ft.Text(reporte["equipo"]))
        celda3 = ft.DataCell(ft.Text(reporte["categoria"]))
        celda4 = ft.DataCell(ft.Text(reporte["fecha"]))
        celda5 = ft.DataCell(ft.Text(reporte["hora"]))
        celda6 = ft.DataCell(ft.Text(reporte["descripcion"]))
        celda7 = ft.DataCell(ft.Text(reporte["encargado"]))
        celda8 = ft.DataCell(ft.Text(reporte["estado"]))
        fila = ft.DataRow(cells=[celda1, celda2, celda3, celda4, celda5, celda6, celda7, celda8])
        lista_tabla.append(fila)

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Etiqueta")),
        ft.DataColumn(ft.Text("Equipo")),
        ft.DataColumn(ft.Text("Categoría")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Hora")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Encargado")),
        ft.DataColumn(ft.Text("Estado")),
    ]

    # Crear la tabla
    tblReportes = ft.DataTable(
        columns=encabezado,
        rows=lista_tabla,
        column_spacing=15,
    )

    # Contenedor para la tabla
    tabla_gestion = ft.ListView(
        controls=[tblReportes],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )


    # Función para mostrar opciones según selección del Navigation Rail
    def mostrar_opcion(e, contenedor):
        seleccion = e.control.selected_index

        if seleccion == 0:
            contenedor.content = principal_colum
        elif seleccion == 1:
            contenedor.content = reservacion_column
        elif seleccion == 2:
            contenedor.content = contenedorTabla
        elif seleccion == 3:
            contenedor.content = gestion_column
        elif seleccion == 4:
            contenedor.content = tabla_gestion
        elif seleccion == 5:
            contenedor.content = ft.Container(content=edit_profile(page, correo))
            page.update()
        elif seleccion == 6:
            main(page)

        page.update()

    # Barra lateral de navegación
    navRail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(label="Página Principal", icon="home"),
            ft.NavigationRailDestination(label="Nueva Reservación", icon="event"),
            ft.NavigationRailDestination(label="Mis Reservaciones", icon="bookmarks_outlined"),
            ft.NavigationRailDestination(label="Nuevo Reporte", icon="note_add_outlined"),
            ft.NavigationRailDestination(label="Gestión De Reportes", icon="report_outlined"),
            ft.NavigationRailDestination(label="Editar Perfil", icon="person_outline"),
            ft.NavigationRailDestination(label="Cerrar Sesión", icon="exit_to_app"),
        ],
        on_change=lambda e: mostrar_opcion(e, contenedorPrincipal),
        width=180,
    )

    contenedorPrincipal = ft.Container(
        content=principal_colum, 
        expand=True
    )

    page.clean()
    page.add(ft.Row([navRail, contenedorPrincipal], expand=True))

# Página principal administrador
def home_admin(page):
    
    # PAGINA USUARIOS

    response = supabase.table("usuario").select("id_usuario, nombre_completo, correo_electronico, division_academica").execute()
    data = response.data  # Datos obtenidos de la tabla

    if not data:
        page.add(ft.Text("No se encontraron datos en la tabla 'usuario'"))
        return

    # Definición de la función para eliminar un registro
    def eliminar_registro_user(e, id_usuario):
        try:
            # Eliminar el usuario por su ID en la base de datos
            supabase.table("usuario").delete().eq("id_usuario", id_usuario).execute()
            # Actualizar la página después de eliminar
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuario con ID {id_usuario} eliminado correctamente."), open=True)
            page.snack_bar.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {str(ex)}"), open=True)
            page.snack_bar.update()

    # Crear la tabla con los datos
    rows = []
    for item in data:
        # Cada fila incluye un botón de eliminar
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["nombre_completo"])),
                    ft.DataCell(ft.Text(item["correo_electronico"])),
                    ft.DataCell(ft.Text(item["division_academica"] or "Sin asignar")),
                    ft.DataCell(
                        ft.ElevatedButton(
                            "Eliminar",
                            on_click=lambda e, id_usuario=item["id_usuario"]: eliminar_registro_user(e, id_usuario),
                        )
                    ),
                ]
            )
        )

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Nombre Completo")),
        ft.DataColumn(ft.Text("Correo Electrónico")),
        ft.DataColumn(ft.Text("División Académica")),
        ft.DataColumn(ft.Text("Acción")),
    ]

    # Crear tabla
    tabla_use = ft.DataTable(
        columns=encabezado,
        rows=rows,
    )

    tabla_users = ft.ListView(
        controls=[tabla_use],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )

        

    # PAGINA PRINCIPAL

    logo_ujat = ft.Image(
    src="admin.png",
    width=250)

    filaLogo = ft.Row([logo_ujat], alignment="center")

    txtBienvenido = ft.Text(
    "¡Bienvenido!", 
    size=28, 
    text_align="center", 
    color="green"
    )

    txtDatos = ft.Text(
        "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, Vhsa, Centro, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00",
        size=14, 
        text_align="center", 
        color="green",
    )

    principal_colum = ft.Column(
        [txtBienvenido, 
         filaLogo, 
         txtDatos],
        # alignment="center",
        alignment=ft.MainAxisAlignment.CENTER,  # Centra el contenido verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido horizontalmente
        spacing=50
    )

    # PAGINA TABLA RESERVACIÓN

    # Obtener datos desde la tabla de reservaciones en Supabase
    response = supabase.table("reservacion").select(
        "id_reservacion, division_academica, licenciatura, asignatura, numero_estudiantes, fecha, hora"
    ).execute()
    data = response.data  # Datos obtenidos de la tabla

    if not data:
        page.add(ft.Text("No se encontraron datos en la tabla 'reservacion'"))
        return

    # Definición de la función para eliminar un registro
    def eliminar_registro(e, id_reservacion):
        try:
            # Eliminar la reservación por su ID en la base de datos
            supabase.table("reservacion").delete().eq("id_reservacion", id_reservacion).execute()
            # Actualizar la página después de eliminar
            page.snack_bar = ft.SnackBar(ft.Text(f"Reservación con ID {id_reservacion} eliminada correctamente."), open=True)
            page.snack_bar.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {str(ex)}"), open=True)
            page.snack_bar.update()

    # Crear la tabla con los datos
    rows = []
    for item in data:
        # Cada fila incluye un botón de eliminar
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["division_academica"] or "Sin asignar")),
                    ft.DataCell(ft.Text(item["licenciatura"] or "Sin asignar")),
                    ft.DataCell(ft.Text(item["asignatura"] or "Sin asignar")),
                    ft.DataCell(ft.Text(str(item["numero_estudiantes"]))),
                    ft.DataCell(ft.Text(item["fecha"])),
                    ft.DataCell(ft.Text(item["hora"])),
                    ft.DataCell(
                        ft.ElevatedButton(
                            "Eliminar",
                            on_click=lambda e, id_reservacion=item["id_reservacion"]: eliminar_registro(e, id_reservacion),
                        )
                    ),
                ]
            )
        )

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("División Académica")),
        ft.DataColumn(ft.Text("Licenciatura")),
        ft.DataColumn(ft.Text("Asignatura")),
        ft.DataColumn(ft.Text("Número de Estudiantes")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Hora")),
        ft.DataColumn(ft.Text("Acción")),
    ]

    # Crear tabla
    tabla_reserva = ft.DataTable(
        columns=encabezado,
        rows=rows,
    )

    tabla_reservaciones = ft.ListView(
        controls=[tabla_reserva],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )




    # PAGINA TABLA EQUIPOS

    response = supabase.table("equipos").select("id, nombre, etiqueta, categoria").execute()
    data = response.data  # Datos obtenidos de la tabla

    if not data:
        page.add(ft.Text("No se encontraron datos en la tabla 'equipos'"))
        return

    # Definición de la función para eliminar un registro
    def eliminar_registro(e, id_equipo):
        try:
            # Eliminar el equipo por su ID en la base de datos
            supabase.table("equipos").delete().eq("id", id_equipo).execute()
            # Actualizar la página después de eliminar
            page.snack_bar = ft.SnackBar(ft.Text(f"Equipo con ID {id_equipo} eliminado correctamente."), open=True)
            page.snack_bar.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {str(ex)}"), open=True)
            page.snack_bar.update()

    # Crear la tabla con los datos
    rows = []
    for item in data:
        # Cada fila incluye un botón de eliminar
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["nombre"])),
                    ft.DataCell(ft.Text(item["etiqueta"])),
                    ft.DataCell(ft.Text(item["categoria"])),
                    ft.DataCell(
                        ft.ElevatedButton(
                            "Eliminar",
                            on_click=lambda e, id_equipo=item["id"]: eliminar_registro(e, id_equipo),
                        )
                    ),
                ]
            )
        )

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Etiqueta")),
        ft.DataColumn(ft.Text("Categoría")),
        ft.DataColumn(ft.Text("Acción")),
    ]

    # Crear tabla
    tabla_eqp = ft.DataTable(
        columns=encabezado,
        rows=rows,
    )

        # Contenedor para la tabla
    tabla_equipo = ft.ListView(
        controls=[tabla_eqp],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )

    

    # PAGINA TABLA REPORTES


    response = supabase.table("reportes").select(
        "id_reporte, etiqueta, equipo, categoria, fecha, hora, descripcion, encargado, estado"
    ).execute()
    data = response.data  # Datos obtenidos de la tabla

    if not data:
        page.add(ft.Text("No se encontraron datos en la tabla 'reportes'"))
        return

    # Definición de la función para eliminar un registro
    def eliminar_registro(e, id_reporte):
        try:
            # Eliminar el reporte por su ID en la base de datos
            supabase.table("reportes").delete().eq("id_reporte", id_reporte).execute()
            # Actualizar la página después de eliminar
            page.snack_bar = ft.SnackBar(ft.Text(f"Reporte con ID {id_reporte} eliminado correctamente."), open=True)
            page.snack_bar.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {str(ex)}"), open=True)
            page.snack_bar.update()

    # Crear la tabla con los datos
    rows = []
    for item in data:
        # Cada fila incluye un botón de eliminar
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["etiqueta"])),
                    ft.DataCell(ft.Text(item["equipo"] or "Sin asignar")),
                    ft.DataCell(ft.Text(item["categoria"] or "Sin asignar")),
                    ft.DataCell(ft.Text(item["fecha"])),
                    ft.DataCell(ft.Text(item["hora"])),
                    ft.DataCell(ft.Text(item["descripcion"])),
                    ft.DataCell(ft.Text(item["encargado"])),
                    ft.DataCell(ft.Text(item["estado"])),
                    ft.DataCell(
                        ft.ElevatedButton(
                            "Eliminar",
                            on_click=lambda e, id_reporte=item["id_reporte"]: eliminar_registro(e, id_reporte),
                        )
                    ),
                ]
            )
        )

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Etiqueta")),
        ft.DataColumn(ft.Text("Equipo")),
        ft.DataColumn(ft.Text("Categoría")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Hora")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Encargado")),
        ft.DataColumn(ft.Text("Estado")),
        ft.DataColumn(ft.Text("Acción")),
    ]

    # Crear tabla
    tabla_report = ft.DataTable(
        columns=encabezado,
        rows=rows,
    )

    tabla_reportes = ft.ListView(
        controls=[tabla_report],
        width=100,  # Ancho fijo para la tabla
        height=500,  # Alto fijo para habilitar scroll si se excede
        expand=False,
    )

    

    # Función para mostrar opciones según selección del Navigation Rail
    def mostrar_opcion(e, contenedor):
        seleccion = e.control.selected_index

        if seleccion == 0:
            contenedor.content = principal_colum
        elif seleccion == 1:
            contenedor.content = tabla_users
        elif seleccion == 2:
            contenedor.content = tabla_reservaciones
        elif seleccion == 3:
            contenedor.content = tabla_equipo
        elif seleccion == 4:
            contenedor.content = tabla_reportes
        elif seleccion == 5:
            main(page)
        page.update()

    # Barra lateral de navegación
    navRail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(label="Página Principal", icon="home_outlined"),
            ft.NavigationRailDestination(label="Usuarios", icon="group_add_outlined"),
            ft.NavigationRailDestination(label="Reservaciónes", icon="event_note_outlined"),
            ft.NavigationRailDestination(label="Equipos", icon="build_outlined"),
            ft.NavigationRailDestination(label="Reportes", icon="report_outlined"),
            # ft.NavigationRailDestination(label="Estadísticas", icon="bar_chart_outlined"),
            ft.NavigationRailDestination(label="Cerrar Sesión", icon="exit_to_app_outlined")

        ],
        on_change=lambda e: mostrar_opcion(e, contenedorPrincipal),
        width=200,
    )

    contenedorPrincipal = ft.Container(
        content=principal_colum, 
        expand=True
    )
    page.clean()
    page.add(ft.Row([navRail, contenedorPrincipal], expand=True))

# Página de inicio de sesión para administradores
def login_admin(page):
    # Variables para almacenar los campos de entrada
    correo_electronico = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.icons.PERSON,
        width=300,
    )

    contrasena = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300,
    )

    # Texto dinámico para las validaciones
    mensaje_validacion = ft.Text(
        "",
        size=12,
        color="red",
        weight="bold",
        text_align="center",
    )

    # Función para manejar el inicio de sesión de administrador
    def handle_login_admin(e):
        correo = str(correo_electronico.value)  # Correo del administrador
        password = str(contrasena.value)  # Contraseña del administrador

        # Validaciones dinámicas
        if not correo.strip():
            mensaje_validacion.value = "El campo 'Correo electrónico' es obligatorio."
            page.update()
        elif correo != "admin@ujat.mx":
            mensaje_validacion.value = "Correo electrónico incorrecto."
            page.update()
        elif not password.strip():
            mensaje_validacion.value = "El campo 'Contraseña' es obligatorio."
            page.update()
        elif password != "admin123":
            mensaje_validacion.value = "Contraseña incorrecta."
            page.update()
        else:
            mensaje_validacion.value = "¡Inicio de sesión exitoso!"
            home_admin(page)
            mensaje_validacion.color = "green"  # Cambia el color si es exitoso
            print("Acceso concedido para:", correo)
            # Aquí puedes agregar la lógica para redirigir a la página del administrador

        page.update()  # Actualizar la página para reflejar los cambios

    # Función para cambiar a la pantalla de login de usuario
    def navigate_to_user_login(e):
        login_screen(page)

    def custom_button():
        return ft.Container(
            content=ft.Text(
                "Acceder",
                size=16,
                color="white",
                weight="bold",
                text_align="center",
                font_family="MontserratBold",
            ),
            bgcolor="#4CAF50",
            border_radius=10,
            alignment=ft.alignment.center,
            padding=ft.Padding(10, 10, 10, 10),
            width=300,
            on_click=handle_login_admin,  # Llamamos a la función para manejar el login
        )

    column = ft.Column(
        [
            ft.Text(
                "ADMINISTRADOR",
                style="headlineSmall",
                text_align="center",
                size=20,
                font_family="MontserratBold",
            ),
            correo_electronico,
            contrasena,
            mensaje_validacion,  # Mostrar el mensaje de validación
            custom_button(),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "¿Eres un usuario?",
                            size=12,
                            weight="normal",
                            color="black",
                        ),
                        ft.Container(
                            content=ft.Text(
                                " Inicia sesión aquí.",
                                size=12,
                                color="blue",
                                weight="bold",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,
                                ),
                            ),
                            on_click=navigate_to_user_login,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    container_with_background = ft.Container(
        content=column,
        width=400,
        height=450,
        bgcolor="#F2F2F2",
        border_radius=10,
        alignment=ft.alignment.center,
        padding=0,
    )

    footer = ft.Container(
        content=ft.Text(
            "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
            "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
            size=12,
            color="white",
            text_align="center",
        ),
        bgcolor="#333333",
        padding=10,
        alignment=ft.alignment.center,
        expand=False,
    )

    main_container = ft.Container(
        content=container_with_background,
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
    )

    page.clean()
    page.add(
        ft.Column(
            [
                main_container,
                footer,
            ],
            expand=True,
            spacing=0,
        )
    )
    page.update()

# Página de aula inmersiva
def aula_inmersiva(page):
    # Contenido informativo sobre el uso del sistema
    info_text = ft.Column(
        controls=[
            ft.Text(
                "Aula Inmersiva UJAT",
                size=32,
                weight=ft.FontWeight.BOLD,
                color="green",
                text_align="center",  # Centrado del título
            ),
            ft.Text(
                "El Aula de Aprendizaje Inmersivo en la División Académica de Ciencias de la Salud (DACS) es un lugar creado "
                "para mejorar los procesos educativos usando tecnología avanzada. Esta aula permite a profesores y estudiantes "
                "acceder a herramientas que enriquecen la enseñanza y el aprendizaje, brindando una experiencia inmersiva que "
                "simula situaciones reales en el campo de la salud.",
                size=18,
                color="black",
                text_align="justify",
                width=500,  # Limitar el ancho del texto para una mejor disposición
            ),
            ft.Text(
                "El aula inmersiva se utiliza para superar las limitaciones en los métodos tradicionales de enseñanza, que pueden "
                "ser insuficientes para cubrir las necesidades prácticas en el área de ciencias de la salud. Este sistema permite "
                "mejorar la preparación de los estudiantes al ofrecerles prácticas más realistas y contextuales antes de enfrentar "
                "situaciones reales con pacientes.",
                size=18,
                color="black",
                text_align="justify",
                width=500,
            ),

        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centrado del texto
        spacing=15,
    )

    # Contenedor para las imágenes
    image_container_1 = ft.Container(
        content=ft.Image(
            src="vr_image1.jpg",  # Cambia a la ruta o URL de tu imagen
            height=200,
            fit=ft.ImageFit.CONTAIN,
        ),
        alignment=ft.alignment.center,
    )

    # Contenedor para la segunda imagen
    image_container_2 = ft.Container(
        content=ft.Image(
            src="vr_image2.jpg",  # Cambia a la ruta o URL de tu imagen
            height=200,
            fit=ft.ImageFit.CONTAIN,
        ),
        alignment=ft.alignment.center,
    )

    # Layout para organizar el texto y las imágenes
    row_layout = ft.Row(
        controls=[
            ft.Column(
                controls=[info_text],
                alignment=ft.MainAxisAlignment.CENTER,  # Centrado del contenido
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            ),
            ft.Container(width=10),  # Reducir el espacio entre las columnas
            ft.Column(
                controls=[image_container_1, image_container_2],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,  # Espaciado más pequeño entre las imágenes
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centrado horizontalmente
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Footer
    footer = ft.Container(
        content=ft.Text(
            "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
            "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
            size=12,
            color="white",
            text_align="center",
        ),
        bgcolor="#333333",
        padding=10,
        alignment=ft.alignment.center,
    )

    btnRegresar = ft.TextButton(
        "Volver",
        icon=ft.icons.ARROW_BACK,  # Icono de flecha de retroceso
        icon_color="green",        # Color del icono (opcional)
        on_click=lambda e: main(page),
    )

    # Agregar contenedor principal y footer a la página
    page.clean()
    page.add(
        btnRegresar,
        ft.Container(
            content=row_layout,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.padding.all(50),  # Ajustar el padding para dar espacio adecuado a los elementos
        ),
        footer,
    )
    page.update()

# Página principal
def main(page: ft.Page):
    page.title = "EDUCONTROL-VR"
    page.controls.clear()
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.padding = 0
    page.spacing = 0
    page.margin = 0

    button_style = ft.ButtonStyle(
        color=ft.colors.WHITE,  # Color blanco para el texto
    )
    
    def navigate_to(destination):
        # Redirigir según el destino
        if destination == "Profesores":
            login_screen(page) 
        elif destination == "Administrador":
            login_admin(page)
        elif destination == "Aula-Inmersiva":
            aula_inmersiva(page)           
        else:
            # Mensaje de navegación para otros botones
            page.snack_bar = ft.SnackBar(ft.Text(f"Navegando a {destination}"))
            page.snack_bar.open()
            page.update()

    def main_page():
        # Restablece la página principal
        page.clean()

        appBar = ft.AppBar(
            leading=ft.Container(
                content=ft.Image(
                    src="logo.jpg",  # Cambia "logo.png" por la ruta de tu imagen
                    width=40,  # Ajusta el tamaño del logo
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                ),
                on_click=lambda _: print("Logo clicked"),
                alignment=ft.alignment.center,  # Centrar la imagen verticalmente
            ),
            title=ft.Text("EDUCONTROL-VR", size=20, font_family="MontserratBold"),
            center_title=True,
            bgcolor="#4BAF4F",
            color="white",
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Aula-Inmersiva",
                            style=button_style,
                            on_click=lambda _: navigate_to("Aula-Inmersiva"),
                        ),
                        ft.VerticalDivider(color=ft.colors.WHITE24, width=1),
                        ft.TextButton(
                            "Profesores",
                            style=button_style,
                            on_click=lambda _: navigate_to("Profesores"),
                        ),
                        ft.VerticalDivider(color=ft.colors.WHITE24, width=1),
                        ft.TextButton(
                            "Administrador",
                            style=button_style,
                            on_click=lambda _: navigate_to("Administrador"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,  # Alineación a la derecha
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        )

        page.appbar = appBar

        left_container = ft.Column(
            controls=[
                ft.Text(
                    "EDUCONTROL-VR",
                    size=45,
                    weight=ft.FontWeight.BOLD,
                    color="green",
                ),
                ft.Text(
                    "Simplifica el control, maximiza la eficiencia.",
                    size=18,
                    italic=True,
                    color="gray",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar texto verticalmente
            spacing=10,
        )

        # Contenedor para la imagen
        right_container = ft.Container(
            content=ft.Image(
                src="principal.png",  # Cambia a la ruta o URL de tu imagen
                width=400,
                height=400,
                fit=ft.ImageFit.CONTAIN,
            ),
            alignment=ft.alignment.center,
        )

        # Contenedor principal que combina texto e imagen
        main_container = ft.Row(
            controls=[
                left_container,
                ft.Container(width=50),
                right_container,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinea horizontalmente al centro
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centra verticalmente
            expand=True,
        )

        footer = ft.Container(
            content=ft.Text(
                "Av. Universidad s/n, Zona de la Cultura, Col. Magisterial, "
                "Villahermosa, Tabasco, Mex. C.P. 86040. Tel (993) 358 15 00!",
                size=12,
                color="white",
                text_align="center",
            ),
            bgcolor="#333333",
            padding=10,
            alignment=ft.alignment.center,
        )

        # Agregar contenedor principal y footer a la página
        page.add(
            ft.Container(
                content=main_container,
                alignment=ft.alignment.center,
                expand=True,
                padding=ft.padding.all(20),
            ),
            footer,
        )
        page.update()

    # Mostrar la página principal al inicio
    main_page()

ft.app(main, view=ft.AppView.WEB_BROWSER)
# ft.app(main)
