"""
Caja de Herramientas Multi-Función - Streamlit
Incluye: Generador de contraseñas, Conversor de dólar, Juego de Snake y
Akinator de animales.

Ejecutar con: streamlit run app.py
"""

import random
import string

import requests
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------
# Configuración general de la página
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Caja de Herramientas",
    page_icon="🛠️",
    layout="centered",
)

MENU_OPCIONES = [
    "🏠 Inicio",
    "🔐 Generador de Contraseñas",
    "💵 Conversor de Dólar",
    "🐍 Juego de Snake",
    "🦁 Akinator de Animales",
]

menu = st.sidebar.radio("Elegí una herramienta", MENU_OPCIONES)

st.sidebar.markdown("---")
st.sidebar.caption("Hecho con Streamlit 🐍")


# ==========================================================================
# 🏠 INICIO
# ==========================================================================
if menu == "🏠 Inicio":
    st.title("🛠️ Caja de Herramientas Multi-Función")
    st.write(
        "Elegí una herramienta desde el menú de la izquierda:"
    )
    st.markdown(
        """
        - 🔐 **Generador de Contraseñas**: crea contraseñas seguras a medida.
        - 💵 **Conversor de Dólar**: convierte USD a otras monedas (con
          cotización en tiempo real o manual).
        - 🐍 **Juego de Snake**: la clásica serpiente, jugable con las
          flechas del teclado.
        - 🦁 **Akinator de Animales**: pensá un animal y la app intenta
          adivinarlo con preguntas de sí/no.
        """
    )


# ==========================================================================
# 🔐 GENERADOR DE CONTRASEÑAS
# ==========================================================================
elif menu == "🔐 Generador de Contraseñas":
    st.header("🔐 Generador de Contraseñas")
    st.write("Configurá las opciones y generá una o varias contraseñas.")

    length = st.slider("Longitud de la contraseña", 4, 64, 12)

    col1, col2 = st.columns(2)
    with col1:
        use_upper = st.checkbox("Incluir mayúsculas (A-Z)", value=True)
        use_lower = st.checkbox("Incluir minúsculas (a-z)", value=True)
    with col2:
        use_digits = st.checkbox("Incluir números (0-9)", value=True)
        use_symbols = st.checkbox("Incluir símbolos (!@#$...)", value=False)

    excluir_ambiguos = st.checkbox(
        "Excluir caracteres ambiguos (l, 1, I, O, 0)", value=False
    )

    cantidad = st.number_input(
        "Cantidad de contraseñas a generar", min_value=1, max_value=20, value=1
    )

    if st.button("🎲 Generar"):
        pool = ""
        if use_upper:
            pool += string.ascii_uppercase
        if use_lower:
            pool += string.ascii_lowercase
        if use_digits:
            pool += string.digits
        if use_symbols:
            pool += string.punctuation

        if excluir_ambiguos:
            for c in "l1IO0":
                pool = pool.replace(c, "")

        if not pool:
            st.error("Tenés que elegir al menos un tipo de carácter.")
        else:
            st.success(f"Se generaron {cantidad} contraseña(s):")
            for _ in range(int(cantidad)):
                password = "".join(random.SystemRandom().choice(pool) for _ in range(length))
                st.code(password, language=None)


# ==========================================================================
# 💵 CONVERSOR DE DÓLAR
# ==========================================================================
elif menu == "💵 Conversor de Dólar":
    st.header("💵 Conversor de Dólar")

    monto = st.number_input("Monto en USD", min_value=0.0, value=100.0, step=1.0)
    moneda_destino = st.selectbox(
        "Moneda destino",
        ["ARS", "EUR", "BRL", "CLP", "UYU", "MXN", "GBP", "JPY"],
    )

    usar_api = st.checkbox(
        "Usar cotización en tiempo real (requiere conexión a internet)",
        value=True,
    )

    rate = None

    if usar_api:
        try:
            resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6)
            data = resp.json()
            if data.get("result") == "success":
                rate = data["rates"].get(moneda_destino)
                if rate:
                    st.success(f"Cotización actual: 1 USD = {rate:.2f} {moneda_destino}")
                else:
                    st.warning(f"No se encontró la moneda {moneda_destino} en la API.")
            else:
                st.warning("La API no devolvió una cotización válida.")
        except Exception:
            st.warning(
                "No se pudo obtener la cotización en tiempo real. "
                "Ingresá el valor manualmente abajo."
            )

    if rate is None:
        rate = st.number_input(
            f"Cotización manual (1 USD = ? {moneda_destino})",
            min_value=0.0,
            value=1000.0,
        )

    if st.button("Convertir"):
        resultado = monto * rate
        st.metric(
            label=f"{monto:.2f} USD equivale a",
            value=f"{resultado:,.2f} {moneda_destino}",
        )


# ==========================================================================
# 🐍 JUEGO DE SNAKE
# ==========================================================================
elif menu == "🐍 Juego de Snake":
    st.header("🐍 Juego de Snake")
    st.write(
        "Hacé clic dentro del recuadro del juego para darle foco y usá las "
        "flechas del teclado (← ↑ → ↓) para moverte. Presioná **R** para "
        "reiniciar cuando pierdas."
    )

    snake_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #111827;
        font-family: sans-serif;
        color: white;
      }
      canvas {
        background: #1f2937;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        margin-top: 10px;
      }
      #score { font-size: 20px; margin-top: 8px; }
      #gameover {
        color: #ff5555;
        font-size: 18px;
        margin-top: 8px;
        min-height: 24px;
      }
    </style>
    </head>
    <body tabindex="0" id="gameBody" onclick="document.getElementById('gameBody').focus();">
    <div id="score">Puntos: 0</div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <div id="gameover"></div>
    <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const box = 20;
    let snake, direction, food, score, game, gameOverFlag;

    function init() {
      snake = [{x: 9 * box, y: 9 * box}];
      direction = null;
      score = 0;
      gameOverFlag = false;
      document.getElementById("score").innerText = "Puntos: 0";
      document.getElementById("gameover").innerText = "";
      placeFood();
      if (game) clearInterval(game);
      game = setInterval(draw, 120);
    }

    function placeFood() {
      food = {
        x: Math.floor(Math.random() * (canvas.width / box)) * box,
        y: Math.floor(Math.random() * (canvas.height / box)) * box,
      };
    }

    document.addEventListener("keydown", (e) => {
      const key = e.key;
      if (key === "ArrowLeft" && direction !== "RIGHT") direction = "LEFT";
      else if (key === "ArrowUp" && direction !== "DOWN") direction = "UP";
      else if (key === "ArrowRight" && direction !== "LEFT") direction = "RIGHT";
      else if (key === "ArrowDown" && direction !== "UP") direction = "DOWN";
      else if ((key === "r" || key === "R") && gameOverFlag) init();
    });

    function draw() {
      ctx.fillStyle = "#1f2937";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = "#e74c3c";
      ctx.fillRect(food.x, food.y, box, box);

      for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = i === 0 ? "#4CAF50" : "#8BC34A";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
        ctx.strokeStyle = "#1f2937";
        ctx.strokeRect(snake[i].x, snake[i].y, box, box);
      }

      if (!direction) return;

      let head = {x: snake[0].x, y: snake[0].y};
      if (direction === "LEFT") head.x -= box;
      if (direction === "UP") head.y -= box;
      if (direction === "RIGHT") head.x += box;
      if (direction === "DOWN") head.y += box;

      const chocoContraPared =
        head.x < 0 || head.x >= canvas.width ||
        head.y < 0 || head.y >= canvas.height;
      const chocoContraSiMismo = snake.some(
        (s) => s.x === head.x && s.y === head.y
      );

      if (chocoContraPared || chocoContraSiMismo) {
        clearInterval(game);
        gameOverFlag = true;
        document.getElementById("gameover").innerText =
          "¡Perdiste! Presioná R para reiniciar";
        return;
      }

      if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById("score").innerText = "Puntos: " + score;
        placeFood();
      } else {
        snake.pop();
      }

      snake.unshift(head);
    }

    document.getElementById("gameBody").focus();
    init();
    </script>
    </body>
    </html>
    """

    components.html(snake_html, height=520)


# ==========================================================================
# 🦁 AKINATOR DE ANIMALES
# ==========================================================================
elif menu == "🦁 Akinator de Animales":
    st.header("🦁 Akinator de Animales 🎩")
    st.write("Pensá un animal y respondé las preguntas con Sí o No.")

    # Árbol de decisión simple. Cada nodo es un dict con "q" (pregunta),
    # "yes" y "no". Las hojas son strings (el animal adivinado).
    animal_tree = {
        "q": "¿Vive principalmente en el agua?",
        "yes": {
            "q": "¿Es un depredador con aletas grandes?",
            "yes": "Tiburón",
            "no": {
                "q": "¿Es un mamífero?",
                "yes": "Delfín",
                "no": "Pez",
            },
        },
        "no": {
            "q": "¿Puede volar?",
            "yes": {
                "q": "¿Sale de noche y usa ecolocalización?",
                "yes": "Murciélago",
                "no": "Águila",
            },
            "no": {
                "q": "¿Es una mascota doméstica común?",
                "yes": {
                    "q": "¿Ladra?",
                    "yes": "Perro",
                    "no": "Gato",
                },
                "no": {
                    "q": "¿Tiene el cuello muy largo?",
                    "yes": "Jirafa",
                    "no": {
                        "q": "¿Tiene rayas blancas y negras?",
                        "yes": "Cebra",
                        "no": {
                            "q": "¿Es muy grande y tiene colmillos o trompa?",
                            "yes": "Elefante",
                            "no": "León",
                        },
                    },
                },
            },
        },
    }

    if "akinator_path" not in st.session_state:
        st.session_state.akinator_path = []

    def obtener_nodo(tree, path):
        nodo = tree
        for paso in path:
            nodo = nodo[paso]
        return nodo

    nodo_actual = obtener_nodo(animal_tree, st.session_state.akinator_path)

    if isinstance(nodo_actual, dict):
        st.subheader(nodo_actual["q"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sí", use_container_width=True):
                st.session_state.akinator_path.append("yes")
                st.rerun()
        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.akinator_path.append("no")
                st.rerun()
    else:
        st.success(f"🎉 ¡Creo que es un(a) **{nodo_actual}**!")
        st.write("¿Adiviné?")

    if st.button("🔄 Reiniciar juego"):
        st.session_state.akinator_path = []
        st.rerun()
