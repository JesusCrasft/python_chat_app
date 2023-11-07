# Python Chat App
> Es una aplicacion que estoy desarrollando para poner en practica mis conocimnientos de Python, Socket y Modulos.
> Es un chat en tiempo real en donde se puede chatear con personas conectadas al mismo servidor, incluso crear grupos.
> Aun falta por pulir algunas cosas y agregar otras por lo que ire actualizando este repositorio de vez en cuando

## Screenshots / Capturas de Pantalla

## Tech-framework used / Tecnologías Usadas
- Python
  - Tkinter
  - Socket
  - Threading
  - JSON
  - OS
  - Pickle
 
## Install / Instalación
#### OS X, Linux y Windows
OS X, Linux y Windows
La libreria OS, Socket, Threading y JSON no son necesarias instalarlas, al instalar python vienen por defecto.

Primer hay que hacer un clone del proyecto de la siguiente forma:

```Shell
git clone https://github.com/JesusCrasft/python_chat_app
```

Luego hay que situarse en la carpeta del clone y instalar las librerias:

```Shell
cd python_chat_app

pip install tk pickle
```

Luego hay 2 alternativas, ejecutar el servidor en la carpeta clone de github o en una diferente, de cualquiera de las dos maneras necesita hacer lo siguiente para que funcione:

En la linea numero 23 llamada "self.SERVER" del archivo "client.py" tiene que colocar la ipv4 de la maquina donde se este ejecutando el servidor.

Luego situandose en la carpeta que contiene el archivo "server.py" tiene que ejecutar el siguiente comando.
```Shell
python server.py
```
Y de la misma forma en la carpeta que contiene el archivo "client.py" tiene que ejecutar el siguiente comando.
```Shell
python client.py
```

## Tasks / Lista de Tareas
- [x] Inicializar repositorio
- [x] Subir mis primeros cambios a GitHub
- [x] Completar el codigo
- [x] Probar el el codigo
- [x] Hacer el readme
- [ ] Terminar los issues pendientes

## Contribute / Para contribuir
1. Has un [Fork](https://github.com/JesusCrasft/python_chat_app/fork)
2. Crea tu propia rama (git checkout -b feature/fooBar)
3. Sube tus cambios (git commit -am 'Add some fooBar')
4. Actualiza tu rama (git push origin feature/fooBar)
5. Has un "Pull Request"

## License / Licencia
Jesus Angulo – @github/JesusCrasft – jesus.flores.angulo@gmail.com
Distributed under the MIT license. See [LICENSE](LICENSE) for more information.
