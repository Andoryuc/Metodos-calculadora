import sympy as sp
import numpy as np
# NUEVO: Importaciones para que entienda el "5x" como "5*x"
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def recoleccion_datos(x: list, f_x: list):
    # zip junta ambas listas paso a paso
    return [list(par) for par in zip(x, f_x)]

def preparar_ecuacion(texto_usuario):
    x = sp.symbols("x")
    
    input_limpio = texto_usuario.replace("^", "**")
    input_limpio = input_limpio.replace("√", "sqrt")
    input_limpio = input_limpio.replace("π", "pi")
    
    # Diccionario que le enseña a SymPy el valor de 'e'
    diccionario_simbolos = {"e": sp.E}
    
    # NUEVO: Activamos la magia para que lea "5x"
    transformaciones = standard_transformations + (implicit_multiplication_application,)
    
    # NUEVO: Usamos parse_expr con las transformaciones en lugar de sympify
    f_expr = parse_expr(input_limpio, local_dict=diccionario_simbolos, transformations=transformaciones)
    
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

def puntos(list_datos, posicion, metodo):
    #posicion 3 y 5 puntos
    """
    x      F(x)
    t      v          dv/dt
    0      1          
    1      1.5
    2      2
    3      2.5
    4      3
    5      4

    Punto central
    F'(x) = (f(x+h) - F(x-h)) / 2h

    F'(2) = (2.5-1.5)/2(1)


    Derecha
        forward
    F(x) = (-3F(x) + 4F(x+h) + F(x+2h)) / 2h

    Izquierda
        Back
    F(x) = (-3F(x) - 4F(x-h) + F(x-2h)) / 2h

    5 puntos
    (-F(x+2h) + 8F(x+h) - 8F(x-h) + F(x-2h)) / 12h
    """
    if len(list_datos) <=2:
        return None, 0
    
    h = (list_datos[1][0] - list_datos[0][0])

    if metodo == "central":
        #formula = (f(x+h) - F(x-h)) / 2h
        if posicion == 0 or posicion == len(list_datos) - 1:
            return None, 1
        soluccion = (list_datos[posicion + 1][1] - list_datos[posicion - 1][1]) / (2 * h)

    elif metodo == "derecha":
        #formula = (-3F(x) + 4F(x+h) + F(x+2h)) / 2h
        if posicion + 2 > len(list_datos) - 1:
            return None, 3
        soluccion = (-3 * list_datos[posicion][1] + 4 * list_datos[posicion + 1][1] - list_datos[posicion + 2][1]) / (2 * h)

    elif metodo == "izquierda":
        #formula = (-3F(x) - 4F(x-h) + F(x-2h)) / 2h
        if posicion - 2 <= -1:
            return None, 2
        soluccion = (3 * list_datos[posicion][1] - 4 * list_datos[posicion - 1][1] + list_datos[posicion - 2][1]) / (2 * h)

    elif metodo == "5 puntos":
        #formula = (-F(x+2h) + 8F(x+h) - 8F(x-h) + F(x-2h)) / 12h
        if posicion - 2 <= -1 or posicion + 2 > len(list_datos) - 1:
            return None, 4
        soluccion = (-list_datos[posicion + 2][1] + 8 * list_datos[posicion + 1][1] - 8 * list_datos[posicion - 1][1] + list_datos[posicion - 2][1]) / (12 * h)

    else:
        return None, 5
    
    return soluccion, -1

def trapecio(list_datos):
    h = (list_datos[1][0] - list_datos[0][0]) / 2

    sum = 0
    for i in range(len(list_datos)):
        sum += 2 * list_datos[i][1]
    
    sum = sum - list_datos[0][1] - list_datos[-1][1]

    resultado = h * sum
    return resultado

def simpson(list_datos):
    """
    (h/3) (f(x0) + 4f(x1) + 2f(x2) + 4f(x3)+...... 4f
    0    2
    1    4
    2    6
    3    8
    4    10
    resultado = 24

    6     120
    8     350
    10    620
    12    820
    14    760
    16    500
    18    200

    x^3 = 64 de 0 a 4

    n>= 4 y que sea de 2 a 2
    """

    #datos

    h = (list_datos[1][0] - list_datos[0][0])

    suma = 0
    for i in range(1, len(list_datos) - 1):
        if (i&1) == 0:
            suma += 2*list_datos[i][1]
        else:
            suma += 4*list_datos[i][1]
    
    #ecuacion
    #if input_seleccion == "ecuacion":

    resultado = (h/3) * (list_datos[0][1] + suma + list_datos[-1][1])
    return resultado

def simpson_ecuacion(expresion, x, a, b, n):
    """
    Calcula la integral de una ecuación usando Simpson 1/3 analíticamente.
    """
    if n % 2 != 0:
        return None, 1

    h = (b - a) / n
    f_a = float(expresion.subs(x, a))
    f_b = float(expresion.subs(x, b))

    suma = f_a + f_b

    for i in range(1, n):
        x_i = a + i * h
        f_xi = float(expresion.subs(x, x_i))
        
        if i % 2 == 0:
            suma += 2 * f_xi
        else:
            suma += 4 * f_xi

    resultado = (h / 3) * suma
    return resultado, -1

# ==========================================
#        NUEVO: MÓDULO CUÁNTICO (Corte 3)
# ==========================================
def regla_fermi(matriz_H_list, vec_f_list, vec_i_list, densidad, usar_constante=False):
    """
    Calcula la probabilidad de transición usando la Regla de Oro de Fermi.
    <f| H' |i>
    """
    # Convertimos las listas a matrices de NumPy
    H = np.array(matriz_H_list, dtype=float)
    f = np.array(vec_f_list, dtype=float)
    i = np.array(vec_i_list, dtype=float)
    
    # Elemento de matriz <f|H'|i> (Multiplicación matricial)
    elemento_matriz = f @ H @ i
    
    # Elevamos al cuadrado el valor absoluto
    M_cuadrado = np.abs(elemento_matriz)**2
    
    # Multiplicamos por la densidad
    resultado_base = M_cuadrado * densidad
    
    # Si el usuario quiere la constante (2pi / h_bar)
    if usar_constante:
        # Nota: h_bar = 1.054571817e-34 (Puedes cambiar este valor según la unidad que uses)
        h_bar = 1.054571817e-34 
        factor_constante = (2 * np.pi) / h_bar
        resultado_final = resultado_base * factor_constante
    else:
        resultado_final = resultado_base
        
    return float(elemento_matriz), float(M_cuadrado), float(resultado_final)