import pandas as pd
import os

NOMBRE_ARCHIVO = "usuarios.csv"

# Columnas requeridas para el sistema
COLUMNAS = [
    "gym_nip",
    "nombre",
    "apellido",
    "edad",
    "telefono",
    "paquete",
    "estatus",
]


def inicializar_archivo():
    """Crea el archivo CSV si no existe en el directorio."""
    if not os.path.exists(NOMBRE_ARCHIVO):
        df_inicial = pd.DataFrame(columns=COLUMNAS)
        df_inicial.to_csv(NOMBRE_ARCHIVO, index=False)


def cargar_datos():
    """Carga los datos desde el CSV a un DataFrame de Pandas."""
    inicializar_archivo()
    return pd.read_csv(NOMBRE_ARCHIVO)


def guardar_datos(df):
    """Guarda el DataFrame de Pandas en el archivo CSV."""
    df.to_csv(NOMBRE_ARCHIVO, index=False)


def obtener_siguiente_nip(df):
    """Calcula el siguiente gym_nip único incremental."""
    if df.empty or "gym_nip" not in df.columns:
        return 1001
    return int(df["gym_nip"].max()) + 1


def registro(df):
    """Agrega un nuevo usuario al gimnasio."""
    print("\n--- ALTA DE NUEVO USUARIO ---")
    gym_nip = obtener_siguiente_nip(df)
    print(f"NIP asignado automáticamente: {gym_nip}")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()

    while True:
        try:
            edad = int(input("Edad: "))
            if edad > 0:
                break
            print("Por favor, ingresa una edad válida.")
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")

    telefono = input("Teléfono: ").strip()

    print("\nPaquetes disponibles:")
    print("1. Básico (Solo pesas)")
    print("2. Completo (Pesas + Cardio)")
    print("3. VIP (Acceso total + Entrenador)")

    opciones_paquete = {"1": "Básico", "2": "Completo", "3": "VIP"}
    while True:
        op_p = input("Selecciona un paquete (1-3): ").strip()
        if op_p in opciones_paquete:
            paquete = opciones_paquete[op_p]
            break
        print("Opción no válida. Intenta de nuevo.")

    nuevo_usuario = {
        "gym_nip": gym_nip,
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "telefono": telefono,
        "paquete": paquete,
        "estatus": "ACTIVO",
    }

    df = pd.concat([df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
    guardar_datos(df)
    print(f"✅ Usuario registrado exitosamente con NIP: {gym_nip}")
    return df


def consulta(df):
    """Muestra el listado de todos los usuarios registrados."""
    print("\n--- CONSULTA GENERAL DE USUARIOS ---")
    if df.empty:
        print("No hay usuarios registrados en el sistema.")
    else:
        print(df.to_string(index=False))


def busqueda(df):
    """Permite buscar usuarios por NIP, Nombre o Estatus."""
    print("\n--- BÚSQUEDA DE USUARIOS ---")
    if df.empty:
        print("El sistema no contiene registros.")
        return

    print("1. Buscar por NIP")
    print("2. Buscar por Nombre")
    print("3. Filtrar por Estatus (ACTIVO/INACTIVO)")
    opcion = input("Selecciona una opción (1-3): ").strip()

    if opcion == "1":
        try:
            nip_buscar = int(input("Ingresa el gym_nip: "))
            resultado = df[df["gym_nip"] == nip_buscar]
            if not resultado.empty:
                print("\n", resultado.to_string(index=False))
            else:
                print("❌ No se encontró ningún usuario con ese NIP.")
        except ValueError:
            print("Error: El NIP debe ser numérico.")

    elif opcion == "2":
        nombre_buscar = input("Ingresa el nombre o coincidencia: ").strip().lower()
        resultado = df[df["nombre"].astype(str).str.lower().str.contains(nombre_buscar)]
        if not resultado.empty:
            print("\n", resultado.to_string(index=False))
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "3":
        estatus_buscar = input("Ingresa estatus (ACTIVO/INACTIVO): ").strip().upper()
        resultado = df[df["estatus"] == estatus_buscar]
        if not resultado.empty:
            print("\n", resultado.to_string(index=False))
        else:
            print(f"❌ No hay usuarios registrados con estatus '{estatus_buscar}'.")
    else:
        print("Opción inválida.")


def modificacion(df):
    """Edita los campos de un usuario existente."""
    print("\n--- MODIFICACIÓN DE DATOS ---")
    if df.empty:
        print("No hay usuarios registrados.")
        return df

    try:
        nip_mod = int(input("Ingresa el gym_nip del usuario a modificar: "))
        indices = df.index[df["gym_nip"] == nip_mod].tolist()

        if not indices:
            print("❌ No existe usuario con ese NIP.")
            return df

        idx = indices[0]
        print("\nDatos actuales del usuario:")
        print(df.loc[[idx]].to_string(index=False))

        print("\n¿Qué campo deseas modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. Edad")
        print("4. Teléfono")
        print("5. Paquete")

        campo_op = input("Selecciona una opción (1-5): ").strip()

        if campo_op == "1":
            df.at[idx, "nombre"] = input("Nuevo nombre: ").strip()
        elif campo_op == "2":
            df.at[idx, "apellido"] = input("Nuevo apellido: ").strip()
        elif campo_op == "3":
            try:
                nueva_edad = int(input("Nueva edad: "))
                if nueva_edad > 0:
                    df.at[idx, "edad"] = nueva_edad
                else:
                    print("Edad no válida.")
                    return df
            except ValueError:
                print("Valor inválido.")
                return df
        elif campo_op == "4":
            df.at[idx, "telefono"] = input("Nuevo teléfono: ").strip()
        elif campo_op == "5":
            print("Paquetes: 1. Básico | 2. Completo | 3. VIP")
            p_op = input("Selecciona (1-3): ").strip()
            paquetes_dict = {"1": "Básico", "2": "Completo", "3": "VIP"}
            if p_op in paquetes_dict:
                df.at[idx, "paquete"] = paquetes_dict[p_op]
            else:
                print("Opción de paquete no válida.")
                return df
        else:
            print("Opción inválida.")
            return df

        guardar_datos(df)
        print("✅ Datos actualizados correctamente.")
    except ValueError:
        print("El NIP debe ser un número entero.")

    return df


def baja(df):
    """Realiza una baja lógica cambiando el estatus a INACTIVO."""
    print("\n--- BAJA LÓGICA DE USUARIO ---")
    if df.empty:
        print("No hay usuarios registrados.")
        return df

    try:
        nip_baja = int(input("Ingresa el gym_nip del usuario a dar de baja: "))
        indices = df.index[df["gym_nip"] == nip_baja].tolist()

        if not indices:
            print("❌ No existe usuario con ese NIP.")
            return df

        idx = indices[0]
        if df.at[idx, "estatus"] == "INACTIVO":
            print("El usuario ya se encuentra con estatus INACTIVO.")
            return df

        confirmacion = input(f"¿Seguro que deseas dar de baja a {df.at[idx, 'nombre']}? (s/n): ").strip().lower()
        if confirmacion == "s":
            df.at[idx, "estatus"] = "INACTIVO"
            guardar_datos(df)
            print("✅ Usuario dado de baja correctamente (Estatus: INACTIVO).")
        else:
            print("Operación cancelada.")

    except ValueError:
        print("El NIP debe ser numérico.")

    return df


def menu():
    """Controla el flujo general de la aplicación."""
    df = cargar_datos()

    while True:
        print("\n==========================================")
        print("  🏋️‍♂️ SISTEMA DE GESTIÓN DE GIMNASIO 🏋️‍♂️  ")
        print("==========================================")
        print("1. Registrar nuevo usuario (Alta)")
        print("2. Consultar lista completa")
        print("3. Buscar usuario")
        print("4. Modificar datos de usuario")
        print("5. Dar de baja usuario (Baja lógica)")
        print("6. Salir")
        print("==========================================")

        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            df = registro(df)
        elif opcion == "2":
            consulta(df)
        elif opcion == "3":
            busqueda(df)
        elif opcion == "4":
            df = modificacion(df)
        elif opcion == "5":
            df = baja(df)
        elif opcion == "6":
            print("\n¡Gracias por utilizar el Sistema de Gestión de Gimnasio! Hasta pronto.")
            break
        else:
            print("Opción no válida. Por favor elige un número entre 1 y 6.")


if __name__ == "__main__":
    menu()
