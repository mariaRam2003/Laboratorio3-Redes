# Laboratorio 3 - Algoritmos de Enrutamiento

**Universidad del Valle de Guatemala**\
**Facultad de Ingeniería**\
**Departamento de Ciencias de la Computación**\
**Redes**


## Autores
- Diego Leiva &emsp;&emsp;&emsp; &ensp; 21752
- Maria Ramirez &emsp;&emsp;&ensp; 21342
- Gustavo Gonzalez &emsp; 21438


## Repositorio
https://github.com/mariaRam2003/Laboratorio3-Redes.git

## Configuración e Instalación
Asegurese de tener los siguientes prerequisitos instalados para utilizar este programa:

- `Python 3.8+` (Recomendado)


### 1. Configuración de Entorno
Puede configurar un entorno virtual usando Venv de Python. Para ello sigua estos pasos:

#### 1.1. Clonar repositorio
Comience por clonar este proyecto desde el repositorio de github
```bash
git clone https://github.com/mariaRam2003/Laboratorio3-Redes.git
```
#### 1.2. Crear entorno virutal
Usando `pip` puede crear y configurar un entorno con **venv**. Para ello navegue al directorio donde pondra el proyecto y cree el entorno con el siguiente comando:
```bash
python -m venv env
```
puede reemplazar `env` por el nombre que desee colocarle a su entorno

#### 1.3. Activación del Entorno
Active el entorno creado con el siguiente comando:

- En Windows:
  ```commandline
  ./env/Scripts/activate
  ```
- En Linux:
  ```bash
  source env/bin/activate
  ```
Nota: Recuerda que si le coloco otro nombre a su entorno debe reemplazar `env` por el nombre que definió.

#### 1.4. Instalar dependencias
Instale las dependencias requeridas desde el archivo de requisitos `requirements.txt` con el siguiente comando:
```bash
pip install -r requirements.txt
```

### 2. Ejecucion del programa
Una vez que haya activado su entorno e instalado las dependencias, debera configurar un archivo `.env` con sus variables de entorno `JID` y `PASSWORD` de su usuario XMPP.

Asimismo debera de configurar los archivos de configuración de topología de red y configuración de nodos. Estos los puede encontrar en la carpeta `files` de este proyecto o si gusta puede utilizar los suyos, y asegurarse de reemplazarlos por los archivos predefinidos dentro de `main.py`

```python
def main():
    config = NetworkConfiguration('files/topo2024-randomX-2024.txt', 'files/names2024-randomX-2024.txt')
```

puede ejecutar el programa desde su IDE de preferencia o desde la consola utilizando el siguiente comando:

```bash
python main.py
```
Este comando iniciara el cliente y generara la topología a partir de sus archivos de configuración.