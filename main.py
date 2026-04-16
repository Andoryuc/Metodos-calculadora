import streamlit as st
import metodos as mt
import streamlit.components.v1 as components  # Aquí importamos tu motor matemático (asegúrate de que tu archivo se llame metodos.py)


# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Calculadora Numérica", page_icon="🧮", layout="centered")
st.title("🧮 Calculadora Numérica")

# --- BLOQUEO DE PANTALLA VERTICAL PRO (Con GIF de rotación) ---
st.markdown("""
    <style>
    /* Ocultamos el mensaje por defecto */
    #pantalla-bloqueo {
        display: none;
    }

    /* Si es un dispositivo móvil (pantalla estrecha) Y está en vertical... */
    @media screen and (max-width: 768px) and (orientation: portrait) {
        #pantalla-bloqueo {
            display: flex !important; /* Forzamos a que se vea */
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #0e1117; /* Fondo oscuro Streamlit */
            z-index: 9999999; /* Por encima de TODO */
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            padding: 30px;
        }
    }
    </style>

    <div id="pantalla-bloqueo">
        <img src="https://yca.org.ar/wp-content/uploads/sites/4/2017/07/rotate.gif" 
             alt="Girar dispositivo" 
             style="max-width: 250px; height: auto; margin-bottom: 20px; border-radius: 10px;">
    </div>
""", unsafe_allow_html=True)

# --- 2. EL MENÚ PRINCIPAL ---
modo_app = st.radio(
    "Selecciona tu modo de trabajo:", 
    ["📐 Modo Ecuaciones (Raíces)", "📊 Modo Tabla de Datos (Integrales/Derivadas)"], 
    horizontal=True
)

st.divider()

# ==========================================
#        MODO 1: ECUACIONES (Corte 1)
# ==========================================
if modo_app == "📐 Modo Ecuaciones (Raíces)":

    # --- 2. LA MEMORIA DE LA CALCULADORA ---
    if 'pantalla' not in st.session_state:
        st.session_state.pantalla = ""

    # NUEVO: Memoria para saber si el teclado alternativo está activo
    if 'teclado_alternativo' not in st.session_state:
        st.session_state.teclado_alternativo = False

    # --- 3. CALLBACKS ---
    def agregar_tecla(simbolo):
        st.session_state.pantalla += simbolo

    def limpiar_pantalla():
        st.session_state.pantalla = ""

    # NUEVO: Callback para borrar solo el último carácter
    def borrar_ultimo():
        if len(st.session_state.pantalla) > 0:
            st.session_state.pantalla = st.session_state.pantalla[:-1]

    # NUEVO: Callback para cambiar entre teclados
    def cambiar_teclado():
        # Invierte el estado: Si es False pasa a True, y viceversa
        st.session_state.teclado_alternativo = not st.session_state.teclado_alternativo

    # --- 4. LA PANTALLA ---
    # Usamos un cuadro de texto desactivado para que el usuario se vea obligado a usar los botones
    st.text_input("Ecuación F(x)", key="pantalla", disabled=False)

    # --- 5. EL TECLADO ---

    # Controles superiores de la calculadora
    col_shift, col_del, col_ac = st.columns([2, 1, 1])
    with col_shift:
        # Este botón cambia el estado de la memoria
        st.button(" 🔄 ", on_click=cambiar_teclado, use_container_width=True)
    with col_del:
        st.button("⌫ DEL", on_click=borrar_ultimo, use_container_width=True)
    with col_ac:
        st.button("AC", on_click=limpiar_pantalla, use_container_width=True)

    # --- 6. EL TECLADO (Botones en columnas para móvil) ---
  
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if not st.session_state.teclado_alternativo:
            st.button(" ^ ", use_container_width=True, on_click=agregar_tecla, args=("^(",))
        else:
            st.button(" √ ", use_container_width=True, on_click=agregar_tecla, args=("√(",))
        st.button("7", use_container_width=True, on_click=agregar_tecla, args=("7",))
        st.button("4", use_container_width=True, on_click=agregar_tecla, args=("4",))
        st.button("1", use_container_width=True, on_click=agregar_tecla, args=("1",))
        st.button("0", use_container_width=True, on_click=agregar_tecla, args=("0",))
        
    with col2:
        if not st.session_state.teclado_alternativo:
            st.button(" π ", use_container_width=True, on_click=agregar_tecla, args=("π",))
        else:
            st.button(" e ", use_container_width=True, on_click=agregar_tecla, args=("e",))
        st.button("8", use_container_width=True, on_click=agregar_tecla, args=("8",))
        st.button("5", use_container_width=True, on_click=agregar_tecla, args=("5",))
        st.button("2", use_container_width=True, on_click=agregar_tecla, args=("2",))
        st.button(".", use_container_width=True, on_click=agregar_tecla, args=(".",))

    with col3:
        if not st.session_state.teclado_alternativo:
            st.button(" ( ", use_container_width=True, on_click=agregar_tecla, args=("(",))
        else:
            st.button(" [ ", use_container_width=True, on_click=agregar_tecla, args=("[",))
        st.button("9", use_container_width=True, on_click=agregar_tecla, args=("9",))
        st.button("6", use_container_width=True, on_click=agregar_tecla, args=("6",))
        st.button("3", use_container_width=True, on_click=agregar_tecla, args=("3",))
        st.button("X", use_container_width=True, on_click=agregar_tecla, args=("x",))

    with col4:
        if not st.session_state.teclado_alternativo:
            st.button(" ) ", use_container_width=True, on_click=agregar_tecla, args=(")",))
        else:
            st.button(" ] ", use_container_width=True, on_click=agregar_tecla, args=("]",))
        st.button(" + ", use_container_width=True, on_click=agregar_tecla, args=("+",))
        st.button(" - ", use_container_width=True, on_click=agregar_tecla, args=("-",))
        st.button(" × ", use_container_width=True, on_click=agregar_tecla, args=("×",))
        st.button(" ÷ ", use_container_width=True, on_click=agregar_tecla, args=("/",))

    with col5:
        if not st.session_state.teclado_alternativo:
            st.button("sin(...)", use_container_width=True, on_click=agregar_tecla, args=("sin(",))
        else:
            st.button("asin(...)", use_container_width=True, on_click=agregar_tecla, args=("asin(",))
        if not st.session_state.teclado_alternativo:
            st.button("cos(...)", use_container_width=True, on_click=agregar_tecla, args=("cos(",))
        else:
            st.button("acos(...)", use_container_width=True, on_click=agregar_tecla, args=("acos(",))
        if not st.session_state.teclado_alternativo:
            st.button("tan(...)", use_container_width=True, on_click=agregar_tecla, args=("tan(",))
        else:
            st.button("atan(...)", use_container_width=True, on_click=agregar_tecla, args=("atan(",))
        if not st.session_state.teclado_alternativo:
            st.button("log(...)", use_container_width=True, on_click=agregar_tecla, args=("log(",))
        else:
            st.button("ln(...)", use_container_width=True, on_click=agregar_tecla, args=("ln(",))
    # --- MENSAJES DE AYUDA (Solo en teclado alternativo) ---
    if st.session_state.teclado_alternativo:
        # Mostramos un mensaje informativo con LaTeX para que se vea matemático
        st.info("💡 **Tip para raíces:** Para calcular una raíz distinta a la cuadrada, usa exponentes fraccionarios. \nPor ejemplo: ⁿ√( ...)^(m) = (...)^(m/n).")
        
    st.divider() # Línea separadora
    
    # ==========================================
    # --- VISUALIZADOR GEOGEBRA (Global para Corte 1) ---
    st.subheader("📊 Visualizador Gráfico")
    st.write("Usa GeoGebra para encontrar tus intervalos (a, b) o tu punto inicial (x0).")
    
    # 1. Creamos una memoria separada exclusiva para la graficadora
    if 'ecuacion_geogebra' not in st.session_state:
        st.session_state.ecuacion_geogebra = ""

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        # 2. Botón de envío manual (Evita que GeoGebra colapse por cada tecla)
        if st.button("📈 Enviar a GeoGebra", use_container_width=True):
            st.session_state.ecuacion_geogebra = st.session_state.pantalla

    # El expander se abre automáticamente si hay una ecuación enviada
    with st.expander("Abrir Graficadora GeoGebra", expanded=True if st.session_state.ecuacion_geogebra else False):
        
        # Limpiamos los símbolos para que la API de Javascript de GeoGebra los entienda
        eq_js = st.session_state.ecuacion_geogebra.replace("π", "pi").replace("√", "sqrt")
        
        # 3. Código mágico usando la API oficial (reemplaza tu antiguo iframe)
        codigo_geogebra = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.geogebra.org/apps/deployggb.js"></script>
        </head>
        <body style="margin:0; padding:0;">
            <div class="applet_container" id="ggb-element" style="width: 100%; height: 500px; border: 1px solid #4B4B4B; border-radius: 8px;"></div>
            <script>
                var params = {{
                    "appName": "graphing", 
                    "width": 800,
                    "height": 500,
                    "scaleContainerClass": "applet_container",
                    "showToolBar": true, 
                    "showAlgebraInput": true, 
                    "showMenuBar": true,
                    // Este es el evento que inyecta la ecuación cuando GeoGebra termina de cargar
                    "appletOnLoad": function(api) {{
                        var ecuacion = "{eq_js}";
                        if(ecuacion.trim() !== "") {{
                            api.evalCommand("f(x) = " + ecuacion);
                        }}
                    }}
                }};
                var applet = new GGBApplet(params, true);
                window.addEventListener("load", function() {{ 
                    applet.inject('ggb-element');
                }});
            </script>
        </body>
        </html>
        """
        # Renderizamos el nuevo componente inteligente
        components.html(codigo_geogebra, height=510)
        
    st.divider() # Otra línea para separar de los métodos
    # ==========================================

    modo_app = st.radio(
    "Selecciona metodo:", 
    ["Bisección", "Newton", "Secante"], 
    horizontal=True
    )

    if modo_app == "Bisección":
        st.subheader("Configuración de Bisección")

        # Streamlit tiene inputs numéricos especiales (reemplazan a tus antiguos inputs de consola)
        col_a, col_b, col_tol = st.columns(3)
        with col_a:
            val_a = st.number_input("Intervalo a", value=0.0, step=None)
        with col_b:
            val_b = st.number_input("Intervalo b", value=0.0, step=None)
        with col_tol:
            val_tol = st.number_input("Tolerancia", value=0.0000000001, step=None, format="%.10f", disabled=True)

        # EL BOTÓN DE ACCIÓN
        if st.button("🚀 Calcular Bisección", type="primary"):
            # 1. Verificamos que no esté vacía
            if st.session_state.pantalla == "":
                st.error("Por favor, ingresa una ecuación primero.")
            else:
                try:
                    # 2. Preparamos la ecuación (usando TU función)
                    expr, var_x = mt.preparar_ecuacion(st.session_state.pantalla)
                    
                    # 3. Calculamos (usando TU función)
                    raiz, iteraciones = mt.bissecion(expr, var_x, val_a, val_b, val_tol)
                    
                    # 4. Mostramos resultados
                    if raiz is None:
                        st.error("🚨 El intervalo no es óptimo (f(a) y f(b) tienen el mismo signo).")
                    else:
                        st.success(f"✅ ¡Raíz encontrada en x = {raiz:.6f}!")
                        st.info(f"Se logró en {iteraciones} iteraciones.")
                        
                except Exception as e:
                    st.error(f"Error en la ecuación. Revisa la sintaxis. (Detalle: {e})")
    
    if modo_app == "Newton":
        st.subheader("Configuración de Newton")

        val_a = st.number_input("Punto x inicial: ", value=0.0, step=None)

        # EL BOTÓN DE ACCIÓN
        if st.button("🚀 Calcular Newton", type="primary"):
            # 1. Verificamos que no esté vacía
            if st.session_state.pantalla == "":
                st.error("Por favor, ingresa una ecuación primero.")
            else:
                try:
                    # 2. Preparamos la ecuación (usando TU función)
                    expr, var_x = mt.preparar_ecuacion(st.session_state.pantalla)
                    
                    # 3. Calculamos (usando TU función)
                    raiz, iteraciones = mt.newton(val_a, expr, var_x)
                    
                    # 4. Mostramos resultados
                    
                    st.success(f"✅ ¡Raíz encontrada en x = {raiz:.6f}!")
                    st.info(f"Se logró en {iteraciones} iteraciones.")
                        
                except Exception as e:
                    st.error(f"Error en la ecuación. Revisa la sintaxis. (Detalle: {e})")

    if modo_app == "Secante":
        st.subheader("Configuración de Secante")

        # Streamlit tiene inputs numéricos especiales (reemplazan a tus antiguos inputs de consola)
        col_a, col_b = st.columns(2)
        with col_a:
            val_a = st.number_input("Primer Dato:", value=0.0, step=None)
        with col_b:
            val_b = st.number_input("Segundo Dato:", value=0.0, step=None)

        # EL BOTÓN DE ACCIÓN
        if st.button("🚀 Calcular Secante", type="primary"):
            # 1. Verificamos que no esté vacía
            if st.session_state.pantalla == "":
                st.error("Por favor, ingresa una ecuación primero.")
            else:
                try:
                    # 2. Preparamos la ecuación (usando TU función)
                    expr, var_x = mt.preparar_ecuacion(st.session_state.pantalla)
                    
                    # 3. Calculamos (usando TU función)
                    ctdr, raiz, f_x = mt.secante(val_a, val_b, expr, var_x)
                    
                    # 4. Mostramos resultados
            
                    st.success(f"✅ ¡Raíz encontrada en x = {raiz:.6f}!")
                    st.info(f"El resultado es: {f_x}.\nSe logró en {ctdr} iteraciones.")
                        
                except Exception as e:
                    st.error(f"Error en la ecuación. Revisa la sintaxis. (Detalle: {e})")

# ==========================================
#        MODO 2: TABLA DE DATOS (Corte 2)
# ==========================================
elif modo_app == "📊 Modo Tabla de Datos (Integrales/Derivadas)":
    import pandas as pd # Importación necesaria para la tabla
    
    st.subheader("Análisis Numérico por Puntos")
    st.write("Ingresa tus datos a continuación. Usa el botón '+' al final de la tabla para agregar más filas.")

    # 1. Memoria de la tabla (Iniciamos con 3 datos de ejemplo para que no dé error inmediato)
    if 'tabla_datos' not in st.session_state:
        st.session_state.tabla_datos = pd.DataFrame({
            "X": [0.0, 0.0, 0.0], 
            "F(X)": [0.0, 0.0, 0.0]
        })

    # 2. El editor mágico de Streamlit
    tabla_editada = st.data_editor(
        st.session_state.tabla_datos, 
        num_rows="dynamic", 
        use_container_width=True
    )

    st.divider()

    # 3. Extracción automática de las columnas a listas de Python
    lista_x = tabla_editada["X"].tolist()
    lista_fx = tabla_editada["F(X)"].tolist()

    # 4. MENÚ DE OPERACIONES DEL CORTE 2
    st.subheader("Configuración del Método")
    
    categoria_metodo = st.radio(
        "¿Qué operación deseas realizar?", 
        ["📈 Derivación Numérica (Puntos)", "📉 Integración Numérica (Área)"], 
        horizontal=True
    )

    # --- LÓGICA DE DERIVACIÓN ---
    if categoria_metodo == "📈 Derivación Numérica (Puntos)":
        col_x, col_tipo = st.columns(2)
        with col_x:
            # Mostramos los valores de X que el usuario escribió en la tabla
            x_elegido = st.selectbox("¿En qué valor de X evaluar la derivada?", lista_x)
        with col_tipo:
            tipo_derivada = st.selectbox("Tipo de Diferencia", ["central", "derecha", "izquierda", "5 puntos"])

        if st.button("🚀 Calcular Derivada", type="primary"):
            # Obtenemos en qué posición (índice 0, 1, 2...) está la X que eligió el usuario
            indice_x = lista_x.index(x_elegido)
            
            # Unimos los datos usando tu función del principio
            datos_emparejados = mt.recoleccion_datos(lista_x, lista_fx)
            
            # Llamamos a tu super función de derivadas
            resultado, cod_error = mt.puntos(datos_emparejados, indice_x, tipo_derivada)
            
            # Manejo maestro de tus códigos de error
            if cod_error == 0:
                st.error("🚨 La tabla debe tener al menos 3 datos.")
            elif cod_error == 1:
                st.error("🚨 Para el método central, necesitas un dato antes y un dato después. No puedes usar los extremos.")
            elif cod_error == 2:
                st.error("🚨 Para hacia atrás (izquierda), necesitas al menos dos datos anteriores en la tabla.")
            elif cod_error == 3:
                st.error("🚨 Para hacia adelante (derecha), necesitas al menos dos datos siguientes en la tabla.")
            elif cod_error == 4:
                st.error("🚨 Para 5 puntos necesitas al menos dos datos antes y dos datos después del punto elegido.")
            elif cod_error == 5:
                st.error("🚨 Método no válido.")
            else:
                st.success(f"✅ La derivada $f'({x_elegido})$ es aproximadamente: **{resultado:.6f}**")

    # --- LÓGICA DE INTEGRACIÓN ---
    elif categoria_metodo == "📉 Integración Numérica (Área)":
        metodo_integral = st.selectbox("Selecciona el método de integración", ["Trapecio", "Simpson 1/3"])
        
        if st.button("🚀 Calcular Integral", type="primary"):
            datos_emparejados = mt.recoleccion_datos(lista_x, lista_fx)
            
            try:
                if metodo_integral == "Trapecio":
                    resultado = mt.trapecio(datos_emparejados)
                    st.success(f"✅ El área aproximada (Trapecio) es: **{resultado:.6f}**")
                    
                elif metodo_integral == "Simpson 1/3":
                    resultado = mt.simpson(datos_emparejados)
                    st.success(f"✅ El área aproximada (Simpson 1/3) es: **{resultado:.6f}**")
                    
            except Exception as e:
                st.error(f"🚨 Hubo un error al calcular la integral. (Detalle: {e})")