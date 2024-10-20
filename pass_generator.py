import random
import json
import os
import hashlib
from colorama import init, Fore, Style
from cryptography.fernet import Fernet

# Inicializar colorama
init(autoreset=True)

# Generar una clave y guardarla en un archivo si no existe
def load_or_generate_key(filename):
    if not os.path.exists(filename):
        key = Fernet.generate_key()
        with open(filename, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(filename, 'rb') as key_file:
            key = key_file.read()
    return key

# Definir los caracteres que se usarán para generar la contraseña
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "!@#$%ˆ&*()_-+=?><"

all_chars = lower + upper + numbers + symbols

# Función para generar la contraseña
def generate_password(length):
    return "".join(random.sample(all_chars, length))

# Función para cargar las credenciales desde un archivo JSON
def load_credentials(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

# Función para guardar las credenciales en un archivo JSON
def save_credentials(filename, credentials):
    with open(filename, 'w') as file:
        json.dump(credentials, file, indent=4)
    print(Fore.GREEN + "La información se ha guardado en 'passwords.json'")

# Función para cifrar un mensaje
def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

# Función para descifrar un mensaje
def decrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.decrypt(message.encode()).decode()

# Función para hashear una descripción
def hash_description(description):
    return hashlib.sha256(description.lower().strip().encode()).hexdigest()

# Función para agregar o actualizar una credencial
def add_or_update_credential(credentials, username, description, password, key):
    hashed_description = hash_description(description)
    encrypted_username = encrypt_message(username, key)
    encrypted_password = encrypt_message(password, key)
    credentials[hashed_description] = {'username': encrypted_username, 'password': encrypted_password}

# Función para recuperar la contraseña
def retrieve_password(credentials, description, key):
    hashed_description = hash_description(description)
    if hashed_description in credentials:
        decrypted_username = decrypt_message(credentials[hashed_description]['username'], key)
        decrypted_password = decrypt_message(credentials[hashed_description]['password'], key)
        print(Style.BRIGHT + Fore.YELLOW + f"Descripción: {description}")
        print(Style.BRIGHT + f"Usuario: {decrypted_username}")
        print(Style.BRIGHT + f"Contraseña: {decrypted_password}")
        print("-" * 20)
    else:
        print(Fore.RED + "No se encontró ninguna coincidencia")

# Función para verificar si una entrada está vacía
def is_valid_input(input_str):
    return bool(input_str and input_str.strip())

# Cargar o generar la clave de cifrado
key_filename = 'secret.key'
key = load_or_generate_key(key_filename)

# Archivo donde se guardarán las credenciales
filename = "passwords.json"
credentials = load_credentials(filename)

# Menú principal
while True:
    print(Style.BRIGHT + Fore.BLUE + "\n" + "=" * 40)
    print(Style.BRIGHT + Fore.CYAN + "  GESTOR DE CONTRASEÑAS")
    print(Style.BRIGHT + Fore.BLUE + "=" * 40)
    print(Style.BRIGHT + "\n1. Generar y guardar una nueva contraseña")
    print("2. Guardar una contraseña ya existente")
    print("3. Recuperar una contraseña")
    print("4. Salir")
    print(Fore.BLUE + "=" * 40)
    choice = input(Fore.CYAN + "Selecciona una opción: ")

    if choice == "1":
        description = input("Introduce una descripción (por ejemplo, el nombre del sitio web o aplicación): ")
        username = input("Introduce el nombre de usuario: ")

        if not is_valid_input(username) or not is_valid_input(description):
            print(Fore.RED + "El nombre de usuario y la descripción no pueden estar vacíos.")
            continue

        hashed_description = hash_description(description)
        if hashed_description in credentials:
            update_choice = input(Fore.YELLOW + "Ya existe una entrada para esta descripción. ¿Deseas actualizar la contraseña? (s/n): ")
            if update_choice.lower() != 's':
                print(Fore.GREEN + "Operación cancelada.")
                continue

        length = int(input("Introduce la longitud de la contraseña: "))
        password = generate_password(length)
        print(Fore.GREEN + f"Contraseña generada: {password}")
        add_or_update_credential(credentials, username, description, password, key)
        save_credentials(filename, credentials)

    elif choice == "2":
        description = input("Introduce una descripción (por ejemplo, el nombre del sitio web o aplicación): ")
        username = input("Introduce el nombre de usuario: ")
        password = input("Introduce la contraseña ya generada: ")

        if not is_valid_input(username) or not is_valid_input(description) or not is_valid_input(password):
            print(Fore.RED + "El nombre de usuario, la descripción y la contraseña no pueden estar vacíos.")
            continue

        hashed_description = hash_description(description)
        if hashed_description in credentials:
            update_choice = input(Fore.YELLOW + "Ya existe una entrada para esta descripción. ¿Deseas actualizar la contraseña? (s/n): ")
            if update_choice.lower() != 's':
                print(Fore.GREEN + "Operación cancelada.")
                continue

        add_or_update_credential(credentials, username, description, password, key)
        save_credentials(filename, credentials)

    elif choice == "3":
        description = input("Introduce la descripción del sitio o aplicación: ")

        if not is_valid_input(description):
            print(Fore.RED + "La descripción no puede estar vacía.")
            continue

        retrieve_password(credentials, description, key)

    elif choice == "4":
        print(Fore.GREEN + "¡Hasta luego!")
        break

    else:
        print(Fore.RED + "Opción no válida, por favor intenta de nuevo.")
