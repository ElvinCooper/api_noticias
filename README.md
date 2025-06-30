[![Test and Deploy](https://github.com/ElvinCooper/api_noticias/actions/workflows/test-and-deploy.yaml/badge.svg)](https://github.com/ElvinCooper/api_noticias/actions/workflows/test-and-deploy.yaml)
---

# 🚀 API RESTful - Gestión de Posts, Favoritos, Categorías y Multimedia

> API desarrollada con **Flask**, usando **JWT** para autenticación, **Flask-Smorest** para documentación y validación, y **SQLAlchemy** para ORM.

---

## 📋 Tecnologías

| Herramienta           | Versión / Uso                      |
| --------------------- | ---------------------------------- |
| 🐍 Python             | 3.x                                |
| 🍶 Flask              | Framework web                      |
| 🔐 Flask-JWT-Extended | Autenticación JWT                  |
| 🗃 SQLAlchemy         | ORM para bases de datos            |
| 🛠 Flask-Smorest      | Documentación OpenAPI / Validación |
| 🎨 Marshmallow        | Serialización y validación         |

---

## ⚙️ Instalación

```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🛠 Configuración

Configura las variables de entorno:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export JWT_SECRET_KEY="tu_secreto_jwt_superseguro"
```

---

## 🚦 Ejecución

```bash
flask run
```

---

## 📡 Endpoints Principales

| Método   | Ruta                          | Descripción                              | Autenticación |
| -------- | ----------------------------- | ---------------------------------------- | ------------- |
| `GET`    | `/categoria`                  | Listar categorías con conteo de posts    | ✅             |
| `POST`   | `/categoria`                  | Crear una nueva categoría                | ✅             |
| `GET`    | `/categoria/<id_categoria>`   | Obtener categoría por ID                 | ✅             |
| `GET`    | `/paises`                     | Listar todos los países                  | ✅             |
| `POST`   | `/paises`                     | Crear un nuevo país                      | ✅             |
| `GET`    | `/paises/<id_pais>`           | Obtener país por ID                      | ✅             |
| `GET`    | `/multimedia`                 | Listar archivos multimedia               | ✅             |
| `POST`   | `/multimedia`                 | Registrar nuevo archivo multimedia       | ✅             |
| `GET`    | `/multimedia/<id_multimedia>` | Obtener archivo multimedia por ID        | ✅             |
| `GET`    | `/favoritos`                  | Listar favoritos del usuario autenticado | ✅             |
| `POST`   | `/favorito/crear`             | Marcar un post como favorito             | ✅             |
| `DELETE` | `/favorito/eliminar`          | Eliminar un post de favoritos            | ✅             |

---

## 🔑 Autenticación

* Todos los endpoints requieren **token JWT**.
* Envía el token en el header:

```
Authorization: Bearer <tu_token>
```

---

## 💡 Ejemplo de Uso

### Crear Categoría

```bash
curl -X POST http://localhost:5000/categoria \
-H "Authorization: Bearer <tu_token>" \
-H "Content-Type: application/json" \
-d '{"descripcion": "Tecnología"}'
```

### Obtener Categorías

```bash
curl -X GET http://localhost:5000/categoria \
-H "Authorization: Bearer <tu_token>"
```

---

## 🧩 Ejemplo Código Python para consumir API (usar requests)

```python
import requests

url = "http://localhost:5000/categoria"
token = "<tu_token>"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Crear categoría
data = {"descripcion": "Deportes"}

response = requests.post(url, headers=headers, json=data)
print(response.json())

# Obtener categorías
response = requests.get(url, headers=headers)
print(response.json())
```

---

## 📂 Estructura del proyecto

```
/app
    /models          # Modelos SQLAlchemy
    /schemas         # Esquemas Marshmallow
    /resources       # Blueprints y rutas
/extensions.py       # Inicialización de extensiones
/app.py             # Punto de entrada
requirements.txt    # Dependencias
README.md           # Documentación
```

---

## 🛡 Manejo de Errores

* Respuestas estándar con códigos HTTP: `400`, `401`, `404`, `409`, `500`.
* Mensajes JSON claros con `"success": false` y `"message"` explicativo.

---

## 📖 Documentación automática

Se genera OpenAPI (Swagger) con **Flask-Smorest**, accesible en:

```
/swagger-ui
```

---
