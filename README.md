# 🛠️ Caja de Herramientas Multi-Función (Streamlit)

Aplicación de Streamlit contenida en un único archivo (`app.py`) que reúne
cuatro mini-herramientas:

1. 🔐 **Generador de Contraseñas**
2. 💵 **Conversor de Dólar**
3. 🐍 **Juego de Snake**
4. 🦁 **Akinator de Animales**

---

## 📋 Requisitos

- Python 3.9 o superior
- Conexión a internet (opcional, solo para la cotización del dólar en tiempo real)

### Dependencias

```bash
pip install streamlit requests
```

---

## ▶️ Cómo ejecutar la app

1. Guardá `app.py` en una carpeta.
2. Abrí una terminal en esa carpeta.
3. Ejecutá:

```bash
streamlit run app.py
```

4. Se abrirá automáticamente en tu navegador (por defecto en
   `http://localhost:8501`).

---

## 🧭 Navegación

La app tiene un menú lateral (sidebar) con 5 secciones:

- 🏠 **Inicio**: pantalla de bienvenida con la descripción de cada herramienta.
- 🔐 **Generador de Contraseñas**
- 💵 **Conversor de Dólar**
- 🐍 **Juego de Snake**
- 🦁 **Akinator de Animales**

---

## 🔐 Generador de Contraseñas

Permite generar una o varias contraseñas seguras eligiendo:

- Longitud (de 4 a 64 caracteres)
- Si incluye mayúsculas, minúsculas, números y/o símbolos
- Exclusión opcional de caracteres ambiguos (`l`, `1`, `I`, `O`, `0`)
- Cantidad de contraseñas a generar de una sola vez

Usa el módulo `random.SystemRandom`, pensado para generar valores
aleatorios más adecuados para contraseñas que el `random` estándar.

---

## 💵 Conversor de Dólar

Convierte un monto en USD a otra moneda (ARS, EUR, BRL, CLP, UYU, MXN, GBP,
JPY).

- Si está tildada la opción **"Usar cotización en tiempo real"**, la app
  consulta la API pública y gratuita
  [open.er-api.com](https://www.exchangerate-api.com/) (no requiere API key).
- Si no hay conexión o la API falla, se puede ingresar la cotización
  manualmente.

> ⚠️ Al no requerir clave, la API pública puede tener límites de uso o
> demoras ocasionales. Por eso siempre hay una alternativa manual.

---

## 🐍 Juego de Snake

Implementado en HTML + JavaScript puro, embebido dentro de Streamlit con
`streamlit.components.v1.html`. Esto permite un juego fluido con captura de
teclado, algo que Streamlit no soporta de forma nativa con widgets de
Python.

**Controles:**

- Flechas del teclado (← ↑ → ↓) para moverse.
- Hacé clic dentro del recuadro del juego primero, para que capture el
  teclado.
- Tecla **R** para reiniciar cuando el juego termina.

---

## 🦁 Akinator de Animales

Mini "adivinador" de animales basado en un árbol de decisión de preguntas de
Sí/No (no usa IA ni conexión a internet). Cada respuesta te acerca a una
hoja del árbol donde la app arriesga un animal.

Incluye botón **"Reiniciar juego"** para volver a empezar en cualquier
momento.

> 💡 Es un árbol fijo y acotado (pensado como demo educativa), no aprende ni
> se actualiza con nuevas respuestas.

---

## 📁 Estructura del proyecto

```
.
├── app.py        # Aplicación completa (todas las herramientas)
└── README.md     # Este archivo
```

---

## 🧩 Posibles mejoras futuras

- Guardar contraseñas generadas en un historial descargable.
- Agregar más monedas y gráficos históricos de cotización.
- Guardar el puntaje máximo del Snake usando `st.session_state`.
- Ampliar el árbol del Akinator o hacerlo dinámico con un dataset más grande.
