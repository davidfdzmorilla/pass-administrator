
# Gestor de Contraseñas

Este proyecto es un **Gestor de Contraseñas** desarrollado en Python que permite generar, guardar, cifrar y recuperar contraseñas de forma segura. Utiliza la librería `cryptography.fernet` para el cifrado y almacenamiento seguro de las credenciales en un archivo JSON.

# Estado de la aplicación

Problemas conocidos:
- El contenedor Docker no puede mostrar la interfaz gráfica de Kivy en sistemas Mac con chip M1/M2, por problemas de compatibilidad con graficos OpenGL. Se está trabajando en una solución.

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

### Clonar el repositorio

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

   - 1. Generar y guardar una nueva contraseña: Crea una nueva contraseña, la cifra y la guarda junto con el nombre de usuario.
   - 2. Guardar una contraseña ya existente: Introduce un nombre de usuario y contraseña ya existente para almacenarla cifrada.
   - 3. Recuperar una contraseña: Proporciona la descripción (sitio o aplicación) para recuperar el nombre de usuario y la contraseña.
   - 4. Salir: Salir del programa.

3. Archivos generados:

   - **secret.key**: Se genera automáticamente para cifrar y descifrar las contraseñas.
   - **passwords.json**: Archivo JSON donde se almacenan las credenciales cifradas.

## Dockerización

### Requisitos

- Docker

### Construir la imagen Docker

Para ejecutar el gestor de contraseñas utilizando Docker, primero necesitas construir la imagen Docker. Esto asegurará que el programa tenga todas las dependencias necesarias sin tener que instalarlas manualmente.

1. Construir la imagen:

    Ejecuta el siguiente comando en el directorio raíz del proyecto (donde está el Dockerfile):

    ```bash
    docker build -t gestor-contrasenas .
    ```

2. Ejecutar el contenedor:

    Una vez que la imagen esté construida, puedes ejecutar el programa dentro de un contenedor Docker con el siguiente comando:

    ```bash
    docker run -it gestor-contrasenas
    ```

### Ejecución de la aplicación con interfaz gráfica (Kivy)

Para que la interfaz gráfica de Kivy funcione en Docker, debes configurar el acceso al sistema de ventanas X11 de tu sistema anfitrión.


Debemos tener instalado el paquete `xhost` en nuestro sistema. Si no lo tienes, puedes instalarlo con el siguiente comando:
* MacOS:
    
```bash
brew install --cask xquartz
```

* Windows:
https://www.xquartz.org/

1. **Permitir acceso a X11** (solo una vez, en tu sistema anfitrión):

    ```bash
    xhost +
    ```

2. **Ejecutar el contenedor con soporte gráfico y peersistencia de daatos con volúmenes**:

    ```bash
    docker run -it --rm \
    --env="DISPLAY" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v $(pwd)/data:/app/data \
    gestor-contrasenas
    ```

Este comando permite que Docker acceda al servidor gráfico X11 para mostrar la interfaz Kivy en tu sistema local y asegura que los archivos generados dentro del contenedor (como las credenciales cifradas) se almacenen en un directorio local llamado `data`.

3. **Desactivar el acceso a X11** (si lo deseas, después de la ejecución):

    ```bash
    xhost -
    ```

### Persistencia de datos con volúmenes

Para mantener los datos (como passwords.json y secret.key) después de reiniciar o parar el contenedor, puedes montar un volumen local:

```bash
docker run -it -v $(pwd)/data:/app gestor-contrasenas
```

Esto asegura que los archivos generados dentro del contenedor (como las credenciales cifradas) se almacenen en un directorio local llamado `data`.

### Ejemplo de uso

Generar y guardar una contraseña nueva:

1. Abrir la aplicación: Una vez que la aplicación se ejecute, verás una ventana donde podrás gestionar las contraseñas.

2. Generar y guardar una nueva contraseña:

    * Introduce la descripción del sitio o aplicación (por ejemplo: "Facebook").
    + Introduce el nombre de usuario (por ejemplo: "usuario123").
    * Haz clic en el botón Generar y Guardar Contraseña.
    * Automáticamente se generará una contraseña segura y se mostrará en un popup.
    * La contraseña y el usuario se cifrarán y se guardarán en el archivo passwords.json.

3. Guardar una contraseña ya existente:

    * Introduce la descripción, el nombre de usuario y la contraseña que deseas guardar.
    * Haz clic en el botón Guardar Contraseña Existente.
    * Los datos se cifrarán y se guardarán en el archivo passwords.json.

4. Recuperar una contraseña:

    * Introduce la descripción del sitio o aplicación.
    * Haz clic en el botón Recuperar Contraseña.
    * La contraseña cifrada se descifrará y se mostrará en un popup.

## Seguridad

Este gestor de contraseñas almacena tus datos cifrados y utiliza una clave de cifrado única generada localmente en el archivo `secret.key`. Es fundamental **mantener este archivo seguro**, ya que cualquier persona con acceso a esta clave puede descifrar las credenciales.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE.md).
