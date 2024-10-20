import random
import json
import os
import hashlib
from cryptography.fernet import Fernet
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

# Definir los caracteres que se usarán para generar la contraseña
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "!@#$%ˆ&*()_-+=?><"

all_chars = lower + upper + numbers + symbols

# Función para generar una contraseña
def generate_password(length):
    return "".join(random.sample(all_chars, length))

# Cargar o generar la clave de cifrado
def load_or_generate_key(filename):
    if not os.path.exists(filename):
        key = Fernet.generate_key()
        with open(filename, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(filename, 'rb') as key_file:
            key = key_file.read()
    return key

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

# Función para cargar credenciales
def load_credentials(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

# Función para guardar credenciales
def save_credentials(filename, credentials):
    with open(filename, 'w') as file:
        json.dump(credentials, file, indent=4)

class PasswordManager(BoxLayout):
    def generate_and_save_password(self):
        description = self.ids.description_input.text
        username = self.ids.username_input.text

        if not description or not username:
            self.show_popup("Error", "La descripción y el usuario no pueden estar vacíos.")
            return

        hashed_description = hash_description(description)
        
        # Verificar si la descripción ya existe
        if hashed_description in self.credentials:
            self.show_confirmation_popup(
                "Advertencia",
                "Ya existe una entrada con esta descripción. ¿Deseas sobrescribirla?",
                lambda: self.save_credential(hashed_description, username, generate_password(16))
            )
        else:
            password = generate_password(16)
            self.save_credential(hashed_description, username, password)

    def save_existing_password(self):
        description = self.ids.description_input.text
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if not description or not username or not password:
            self.show_popup("Error", "Todos los campos son obligatorios.")
            return

        hashed_description = hash_description(description)
        
        if hashed_description in self.credentials:
            self.show_confirmation_popup(
                "Advertencia",
                "Ya existe una entrada con esta descripción.\n¿Deseas sobrescribirla?",
                lambda: self.save_credential(
                    hashed_description, 
                    username, 
                    password
                )
            )
        else:
            self.save_credential(
                hashed_description, 
                username, 
                password
            )


    def save_credential(self, hashed_description, username, password):
        encrypted_username = encrypt_message(username, self.key)
        encrypted_password = encrypt_message(password, self.key)

        self.credentials[hashed_description] = {'username': encrypted_username, 'password': encrypted_password}
        save_credentials(self.credentials_filename, self.credentials)

        self.show_popup("Éxito", f"Contraseña guardada correctamente: \n\n{password}")
        self.clear_inputs()

    def retrieve_password(self):
        description = self.ids.description_input.text

        if not description:
            self.show_popup("Error", "La descripción no puede estar vacía.")
            return

        hashed_description = hash_description(description)
        if hashed_description in self.credentials:
            decrypted_username = decrypt_message(self.credentials[hashed_description]['username'], self.key)
            decrypted_password = decrypt_message(self.credentials[hashed_description]['password'], self.key)
            self.show_popup("Recuperar Contraseña", f"Usuario: {decrypted_username}\n\nContraseña: {decrypted_password}")
        else:
            self.show_popup("Error", "No se encontró ninguna coincidencia.")

    def show_confirmation_popup(self, title, message, confirm_callback):
        popup_content = BoxLayout(orientation='vertical')
        
        # Habilitar el ajuste de texto para el Label
        label = Label(
            text=message, 
            font_size=28, 
            halign="center", 
            valign="middle", 
            text_size=(500, None)  # Asegura que el texto se ajuste y permita saltos de línea
        )
        label.bind(size=label.setter('text_size'))  # Actualizar el tamaño del texto según el tamaño del Label

        popup_content.add_widget(label)
        
        buttons_layout = BoxLayout(size_hint_y=None, height=50)
        
        confirm_button = Button(text="Sobrescribir", on_press=lambda x: [confirm_callback(), popup.dismiss()])
        cancel_button = Button(text="Cancelar", on_press=lambda x: popup.dismiss())
        
        buttons_layout.add_widget(confirm_button)
        buttons_layout.add_widget(cancel_button)
        
        popup_content.add_widget(buttons_layout)
        
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(None, None),
            size=(600, 400)
        )
        popup.open()


    def show_popup(self, title, message):
        popup_content = Label(text=message, font_size=28)
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(None, None),
            size=(600, 400)
        )
        popup.open()

    def clear_inputs(self):
        self.ids.description_input.text = ''
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_filename = 'secret.key'
        self.credentials_filename = 'passwords.json'
        self.key = load_or_generate_key(self.key_filename)
        self.credentials = load_credentials(self.credentials_filename)

class PasswordManagerApp(App):
    def build(self):
        return PasswordManager()

if __name__ == '__main__':
    PasswordManagerApp().run()
