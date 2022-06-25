# Proyecto de Big Data 2022-1
## Estudiantes:

- Ariana
- Roosevelt
- Stephano
- Victor

## ¿Como configurar el proyecto?

## Usando VirtualEnv

- Crear un virtualenv en python

```bash
python3 -m venv venv
source venv/bin/activate
```

- Instalar dependencias

```bash
pip install -r requirements.txt
```

- Ejecutar el proyecto
  
```bash
cd src/
python3 main.py
```

### Usando Conda

- Crear un conda envrionment para el proyecto

```bash
conda env create -f environment.yml
```

- Activar el conda environment

```bash
conda activate proyecto-bigdata-2022-1
```

- Ejecutar el proyecto
  
```bash
cd src/
python3 main.py
```

## Estructura del Proyecto

- `src/generator.py`: generador de temporal events
- `src/dhpg.py`: Distributed Hierarchical Pattern Graph (DHPG)
- `src/node.py`: clase nodo para el DHPG
- `src/utils.py`: funciones utilitarias
- `src/main.py`: archivo de ejecución principal