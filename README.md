# Gestor de Contraseñas

Este proyecto es un **Gestor de Contraseñas** desarrollado en Python que permite generar, guardar, cifrar y recuperar contraseñas de forma segura. Utiliza la librería `cryptography.fernet` para el cifrado y almacenamiento seguro de las credenciales en un archivo JSON.

## Características

- **Generación de contraseñas seguras**: Genera contraseñas aleatorias con combinaciones de letras mayúsculas, minúsculas, números y símbolos.
- **Cifrado de credenciales**: Cifra tanto los nombres de usuario como las contraseñas utilizando la librería `Fernet`.
- **Gestión de credenciales**: Permite agregar, actualizar y recuperar contraseñas de forma fácil y segura.
- **Interfaz interactiva**: Menú fácil de usar para gestionar tus credenciales.

## Instalación

### Requisitos

- Python 3.x
- Las siguientes librerías de Python:
  - `cryptography`
  - `colorama`

Para instalar las dependencias, puedes ejecutar:

```bash
pip install cryptography colorama
```

Clonar el repositorio

```bash

git clone https://github.com/usuario/gestor-de-contrasenas.git
cd gestor-de-contrasenas

```

## Uso sin Docker

1. Ejecutar el programa: Ejecuta el siguiente comando en la terminal:

```bash

python gestor_contrasenas.py

```

2. Opciones disponibles:

    1. Generar y guardar una nueva contraseña: Crea una nueva contraseña, la cifra y la guarda junto con el nombre de usuario.
    2. Guardar una contraseña ya existente: Introduce un nombre de usuario y contraseña ya existente para almacenarla cifrada.
    3. Recuperar una contraseña: Proporciona la descripción (sitio o aplicación) para recuperar el nombre de usuario y la contraseña.
    4. Salir: Salir del programa.

3. Archivos generados:

secret.key: Se genera automáticamente para cifrar y descifrar las contraseñas.

passwords.json: Archivo JSON donde se almacenan las credenciales cifradas.

## Dockerización

### Requisitos

* Docker

### Construir la imagen Docker

Para ejecutar el gestor de contraseñas utilizando Docker, primero necesitas construir la imagen Docker. Esto asegurará que el programa tenga todas las dependencias necesarias sin tener que instalarlas manualmente.

1. Construir la imagen:

    Ejecuta el siguiente comando en el directorio raíz del proyecto (donde está el Dockerfile):

    ```bash

    docker build -t gestor-contrasenas .

    ````

2. Ejecutar el contenedor:

    Una vez que la imagen esté construida, puedes ejecutar el programa dentro de un contenedor Docker con el siguiente comando:

    ````

    docker run -it gestor-contrasenas

    ````

### Persistencia de datos con volúmenes

Para mantener los datos (como passwords.json y secret.key) después de reiniciar o parar el contenedor, puedes montar un volumen local:

``` bash

docker run -it -v $(pwd)/data:/app gestor-contrasenas

```

Esto asegura que los archivos generados dentro del contenedor (como las credenciales cifradas) se almacenen en un directorio local llamado data.

### Ejemplo de uso

Generar y guardar una contraseña nueva

```bash

Selecciona una opción: 1

Introduce una descripción (por ejemplo, el nombre del sitio web o aplicación): Facebook

Introduce el nombre de usuario: usuario123

Introduce la longitud de la contraseña: 16

Contraseña generada: A1b2C3d4E5f6G7h8

La información se ha guardado en 'passwords.json'

```

Recuperar una contraseña

``` bash

Selecciona una opción: 3

Introduce la descripción del sitio o aplicación: Facebook

Descripción: Facebook

Usuario: usuario123
Contraseña: A1b2C3d4E5f6G7h8

```

### Seguridad

Este gestor de contraseñas almacena tus datos cifrados y utiliza una clave de cifrado única generada localmente en el archivo secret.key. Es fundamental mantener este archivo seguro, ya que cualquier persona con acceso a esta clave puede descifrar las credenciales.


Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE.md).