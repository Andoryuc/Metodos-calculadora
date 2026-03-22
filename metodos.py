import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import asyncio

while True:
    input_seleccion_corte = input("Ingrese el corte (1, 2): ")
    if input_seleccion_corte in ["1", "2"]:
        break
    print("Error: Ingrese entre los cortes 1 o 2")

def numero_entero(texto):
    while True:
        try:
            input_numero = int(input(texto))
            return input_numero
        except ValueError:
            print("Ingrese solo numeros enteros")

def numero_float(texto):
    while True:
        try:
            input_numero = float(input(texto))
            return input_numero
        except ValueError:
            print("Ingrese solo numeros")

def numero_positivo(texto):
    while True:
        try:
            input_numero = int(input(texto))
            if input_numero >= 0:
                return input_numero
            else:
                print("Error: Ingrese un numero entero positivo")
        except ValueError:
            print("Ingrese solo numeros enteros")

def recoleccion_datos(texto):
    input_cantidad_datos = numero_positivo(texto)

    list_datos = []
    for i in range(input_cantidad_datos):
        list_borrador = []
        input_datos_x = numero_float(f"Ingrese el {i+1} x: ")
        input_datos_f_x = numero_float(f"Ingrese el {i+1} F(x): ")
        list_borrador.append(input_datos_x)
        list_borrador.append(input_datos_f_x)
        list_datos.append(list_borrador)
    return list_datos

def preparar_ecuacion(texto_usuario):
    x = sp.symbols("x")
    # Limpiamos y convertimos el texto que YA recibimos
    input_limpio = texto_usuario.replace("^", "**")
    f_expr = sp.sympify(input_limpio)
    return f_expr, x

def bissecion(f_expr, x, a, b, error_tol):
    # --- MÉTODO DE BISECCIÓN ---
    """

    1. tomamos un intervalo

    2. verificamos que f(a) * f(b) < 0

    3. calculamos el punto medio. Formula c = (a+b) / 2

    4. evaluamos f(c)

    5. evaluamos el intervalo donde hay cambio de signo

    6. Esto se repite hasta que logremos cumplir con el cometido

    n > log((b-a)/e) numero de interacciones para la tolerancia

    """
    # Evaluamos usando .subs() para sustituir la x por el valor numérico
    f_a = float(f_expr.subs(x, a))
    f_b = float(f_expr.subs(x, b))

    if f_a * f_b >= 0:
        return None, 0

    # Calculamos iteraciones: log2((b-a)/e)
    iteraciones = int(np.ceil(np.log2((b - a) / error_tol)))

    for i in range(iteraciones):
        c = (a + b) / 2
        f_c = float(f_expr.subs(x, c))
        
        if f_a * f_c < 0:
            b = c
        else:
            a = c
            f_a = f_c
    
    raiz = (a + b) / 2
    
    return raiz, iteraciones

def newton(x0, f_expr, x):
        # --- MÉTODO DE NEWTON ---
    df_expr = sp.diff(f_expr, x)
    
    temp_x = x0
    
    i = 1

    while True:
        f_val = float(f_expr.subs(x, temp_x))
        df_val = float(df_expr.subs(x, temp_x))
        
        if df_val == 0:
            return None, 0
            
        nuevo_x = temp_x - (f_val / df_val)
        
        if round(nuevo_x, 10) == round(temp_x, 10):
            break
        
        temp_x = nuevo_x
        i = i + 1
        
    raiz = temp_x
    return raiz, df_val, i

def secante(input_datoH1, input_datoH2, f_expr, x):
    dato1 = input_datoH1
    dato2 = input_datoH2

    for ctdr in range(1, 101):
        r_dato2_1 = dato2

        f_val1 = float(f_expr.subs(x, dato1))
        f_val2 = float(f_expr.subs(x, dato2))

        dato2 = dato2 - f_val2 * ((dato2 - dato1)/(f_val2 - f_val1))
        if (f_val2 - f_val1) == 0: return None, 0, ctdr

        dato1 = r_dato2_1

        f_val2 = float(f_expr.subs(x, dato2))
        
        if abs(f_val2) < 1e-10:
            return ctdr, dato2, f_val2
    return None, dato2, f_val2