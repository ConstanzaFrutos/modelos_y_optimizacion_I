#!/usr/bin/env python3

'''
Script para generar el archivo .dat en formato GLPK para el TP de modelos.
'''

######################### DATOS A GENERAR ######################################
DATA = [
#     1    2    3    4    5    6    7    8    9    10
    [' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', 'F'], # J
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], # I
    [' ', ' ', 'E', ' ', 'E', ' ', 'E', 'E', ' ', ' '], # H
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', 'E', ' '], # G
    [' ', ' ', 'E', ' ', 'E', ' ', ' ', ' ', ' ', ' '], # F
    [' ', 'E', ' ', ' ', ' ', 'E', ' ', 'E', ' ', ' '], # E
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' '], # D
    [' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', 'E'], # C
    [' ', 'E', ' ', 'E', 'E', ' ', 'E', ' ', ' ', ' '], # B
    ['C', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ']  # A
#     1    2    3    4    5    6    7    8    9    10
]

INCLUIR_TIEMPOS = True

TIEMPO_MAXIMO = 120
CAPACIDAD_COMBI = 15
N_COMBIS = 3
COSTO_KM = 1
COSTO_COMBI = 10
###############################################################################

ID_EMPLEADOS = {}
POSICIONES_EMPLEADOS = {}
POSICION_COMBI_INICIAL = 0
POSICION_FABRICA = 21
e = 0
for f in range(len(DATA)):
    for c in range(len(DATA[0])):
        if DATA[f][c] == 'E':
            POSICIONES_EMPLEADOS[e] = (f, c)
            ID_EMPLEADOS[e] = chr(len(DATA) - 1 - f + ord('A')) + str(c + 1)
            e += 1
        elif DATA[f][c] == 'C':
            POSICION_COMBI_INICIAL = (f, c)
        elif DATA[f][c] == 'F':
            POSICION_FABRICA = (f, c)


N_EMPLEADOS = len(POSICIONES_EMPLEADOS)

DISTANCIAS = [ 
    [ 0 for f in range(len(POSICIONES_EMPLEADOS) + 1) ] for c in range(len(POSICIONES_EMPLEADOS) + 1) 
]

for e1 in range(len(DISTANCIAS)):
    for e2 in range(len(DISTANCIAS[e1])):
        if e1 == e2:
            DISTANCIAS[e1][e1] = '.'
            continue
        if e1 == 0:
            f1, c1 = POSICION_COMBI_INICIAL
        else:
            f1, c1 = POSICIONES_EMPLEADOS[e1 - 1]
        if e2 == 0:
            f2, c2 = POSICION_COMBI_INICIAL
        else:
            f2, c2 = POSICIONES_EMPLEADOS[e2 - 1]

        distancia = abs(f1 - f2) + abs(c1 - c2)
        DISTANCIAS[e1][e2] = DISTANCIAS[e2][e1] = distancia

TIEMPO_POR_CASILLA = 2
TIEMPOS = [ 
    [ 0 for f in range(len(POSICIONES_EMPLEADOS) + 1) ] for c in range(len(POSICIONES_EMPLEADOS) + 1) 
]

for e1 in range(len(TIEMPOS)):
    for e2 in range(len(TIEMPOS[e1])):
        if e1 == e2:
            TIEMPOS[e1][e1] = '.'
            continue

        tiempo = TIEMPO_POR_CASILLA * DISTANCIAS[e1][e2]
        TIEMPOS[e1][e2] = tiempo

# Generar archivo .dat
print('data;')
print()
print('# Combis disponibles')
print('set COMBIS := ' + ' '.join(map(str, range(1, N_COMBIS + 1))) + ';')
print()
print('# Empleados a recoger')
print('set EMPLEADOS := ' + ' '.join(map(str, range(1, N_EMPLEADOS + 1))) +  ';')
print()
print('# Lugares a visitar, empleados (1, 2, ...) + empresa (0)')
print('set LUGARES := 0 ' + ' '.join(map(str, range(1, N_EMPLEADOS + 1))) +  ';')
print()
print('# Matriz de distancias entre lugares')
param_d = 'param D : ' + ''.join('{:>4}'.format(i) for i in range(len(DISTANCIAS))) + ' :=\n'
for i, fila in enumerate(DISTANCIAS):
    param_d += f'       {i:2} ' + ''.join('{:>4}'.format(i) for i in fila) + '\n'
param_d = param_d.rstrip('\n') + ';'

print(param_d)
print()

if INCLUIR_TIEMPOS:
    print('# Tiempos de viaje entre lugares')

    param_t = 'param T : ' + ''.join('{:>4}'.format(i) for i in range(len(TIEMPOS))) + ' :=\n'
    for i, fila in enumerate(TIEMPOS):
        param_t += f'       {i:2} ' + ''.join('{:>4}'.format(i) for i in fila) + '\n'
    param_t = param_t.rstrip('\n') + ';'

    print(param_t)
    print()

print('# Número grande en el contexto del modelo')
print('param M := 100000;')
print()
print('# Capacidad máxima de cada combi, en pasajeros')
print(f'param CAPMAX := {CAPACIDAD_COMBI};')
print()
print('# Costo por kilómetro recorrido')
print(f'param CKM := {COSTO_KM};')
print()
print('# Costo por día de contratar una combi')
print(f'param CCOMBI := {COSTO_COMBI};')
print()
print('# Tiempo máximo de viaje desde que se recoge al primer empleado, en minutos')
print(f'param TMAX := {TIEMPO_MAXIMO};')

print('end;')