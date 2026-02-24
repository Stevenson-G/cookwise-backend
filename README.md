# Cookwise Backend

Backend de la aplicación **Cookwise**, una red social de recetas desarrollada como proyecto académico (TFG).

Este backend está construido con arquitectura modular, autenticación segura mediante JWT y base de datos PostgreSQL.

---

## Tecnologías utilizadas

- FastAPI  
- PostgreSQL  
- SQLAlchemy (ORM)  
- JWT Authentication  
- Passlib (bcrypt)  
- Pydantic  
- Uvicorn  

---


## Requisitos previos

- Python 3.10 o superior  
- PostgreSQL instalado y en ejecución  
- Git  

---

## Instalación

1. Clonar el repositorio:

git clone https://github.com/Stevenson-G/cookwise-backend.git  
cd cookwise-backend  

2. Crear entorno virtual:

python -m venv venv  

Activar entorno:

Windows:  
venv\Scripts\activate  

Mac/Linux:  
source venv/bin/activate  

3. Instalar dependencias:

pip install -r requirements.txt  

---

## Configuración de base de datos

Crear base de datos en PostgreSQL:

CREATE DATABASE cookwise;

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/cookwise  
SECRET_KEY=supersecretkey  

Reemplazar:
- TU_PASSWORD → contraseña real de PostgreSQL  
- supersecretkey → una clave secreta segura  

---

## Ejecutar servidor

python -m uvicorn app.main:app --reload  

API disponible en:

http://127.0.0.1:8000  

Documentación Swagger:

http://127.0.0.1:8000/docs  

---

## Sistema de autenticación

El backend implementa:

- Registro de usuarios  
- Login  
- Generación de JWT  
- Hash seguro de contraseñas  
- Conexión a PostgreSQL  

---
