import numpy as np

def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]

def determinarArmadura(pitches):
     
    # Creamos un string vacio que llenaremos 
    # con las notas que predominan en la cancion
    
    string_pitches = ''
    if (pitches['A'] > pitches['Ab']):
        string_pitches = string_pitches + 'A'
    else:
        string_pitches = string_pitches + 'H'
        
    if (pitches['B'] > pitches['Bb']):
        string_pitches = string_pitches + 'B'
    elif (pitches['Bb'] > pitches['A']):
        string_pitches = string_pitches + 'I'
    else:
        string_pitches = string_pitches + 'A'
    
    if (pitches['C'] > pitches['Db']):    
        string_pitches = string_pitches + 'C'
    elif (pitches['C']) > pitches['B']:
        string_pitches = string_pitches + 'O'
    else:
        string_pitches = string_pitches + 'B'
        
    if (pitches['D'] > pitches['Db']):
        string_pitches = string_pitches + 'D'
    else:
        string_pitches = string_pitches + 'J'
        
    if (pitches['E'] > pitches['Eb']):
        string_pitches = string_pitches + 'E'
    elif (pitches ['Eb'] > pitches['D']):
        string_pitches = string_pitches + 'K'
    else:
        string_pitches = string_pitches + 'D'
        
    if (pitches['F'] > pitches['Gb']):
        string_pitches = string_pitches + 'F'
    elif (pitches['F'] > pitches['E']):
        string_pitches = string_pitches + 'P'
    else:
        string_pitches = string_pitches + 'E'
        
    if (pitches['G'] > pitches['Gb']):
        string_pitches = string_pitches + 'G'
    else:
        string_pitches = string_pitches + 'L'
    
    return string_pitches

def dominante(pitches, dickey):
    # Creamos una lista vacia que llenaremos a partir del diccionario de pitches
    # que contenga unicamente los elementos de listakey
    
    pkey = {}
    
    # Lennamos las escalas menores
    pkey['Abm'] = pitches[dickey['Abm']]
    pkey['Am'] = pitches[dickey['Am']]
    pkey['Bbm'] = pitches[dickey['Bbm']]
    pkey['Bm'] = pitches[dickey['Bm']]
    pkey['Cm'] = pitches[dickey['Cm']]
    pkey['Dbm'] = pitches[dickey['Dbm']]
    pkey['Dm'] = pitches[dickey['Dm']]
    pkey['Ebm'] = pitches[dickey['Ebm']]
    pkey['Em'] = pitches[dickey['Em']]
    pkey['Fm'] = pitches[dickey['Fm']]
    pkey['Gbm'] = pitches[dickey['Gbm']]
    pkey['Gm'] = pitches[dickey['Gm']]

    # Llenamos las escalas menores
    pkey['Ab'] = pitches[dickey['Ab']]
    pkey['A'] = pitches[dickey['A']]
    pkey['Bb'] = pitches[dickey['Bb']]
    pkey['B'] = pitches[dickey['B']]
    pkey['C'] = pitches[dickey['C']]
    pkey['Db'] = pitches[dickey['Db']]
    pkey['D'] = pitches[dickey['D']]
    pkey['Eb'] = pitches[dickey['Eb']]
    pkey['E'] = pitches[dickey['E']]
    pkey['F'] = pitches[dickey['F']]
    pkey['Gb'] = pitches[dickey['Gb']]
    pkey['G'] = pitches[dickey['G']]
    
    return pkey

def compararKey(string_pitches, dmax, dickey):
    
    X = dickey.copy()
    
    # Comparamos el string obtenido con el correspondiente a
    # cierta tonalidad, y medimos su distancia de Levenshtein.
    
    # Si la distancia es menor igual a dmax, asignamos esa tonalidad
    
    # Probemos si la tonalidad corresponde a menores, que tienen su respectiva
    # relacion con una escala mayor
    d_Ab = levenshteinDistanceDP(string_pitches, "HIBJKEL")
    d_A = levenshteinDistanceDP(string_pitches, "ABCDEFG")
    d_Bb = levenshteinDistanceDP(string_pitches, "HICJKFL")
    d_B = levenshteinDistanceDP(string_pitches, "ABODEPG")
    d_C = levenshteinDistanceDP(string_pitches, "HICDKFG")
    d_Db = levenshteinDistanceDP(string_pitches, "HABJKEL")
    d_D = levenshteinDistanceDP(string_pitches, "AICDEFG")
    d_Eb = levenshteinDistanceDP(string_pitches, "HIBJKFL")
    d_E = levenshteinDistanceDP(string_pitches, "ABCDEPG")
    d_F = levenshteinDistanceDP(string_pitches, "HICJKFG")
    d_Gb = levenshteinDistanceDP(string_pitches, "HABJDEL")
    d_G = levenshteinDistanceDP(string_pitches, "AICDKFG")

    
    if (d_Ab <= dmax):
        dickey['Abm'] = 'Ab'
        dickey['B'] = 'B'
    if (d_A <= dmax):
        dickey['Am'] = 'A'
        dickey['C'] = 'C'
    if (d_Bb <= dmax):
        dickey['Bbm'] = 'Bb'
        dickey['Db'] = 'Db'
    if (d_B <= dmax):
        dickey['Bm'] = 'B'
        dickey['D'] = 'D'
    if (d_C <= dmax):
        dickey['Cm'] = 'C'
        dickey['Eb'] = 'Eb'
    if (d_Db <= dmax):
        dickey['Dbm'] = 'Db'
        dickey['E'] = 'E'
    if (d_D <= dmax):
        dickey['Dm'] = 'D'
        dickey['F'] = 'F'
    if (d_Eb <= dmax):
        dickey['Ebm'] = 'Eb'
        dickey['Gb'] = 'Gb'
    if (d_E <= dmax):
        dickey['Em'] = 'E'
        dickey['G'] = 'G'
    if (d_F <= dmax):
        dickey['Fm'] = 'F'
        dickey['Ab'] = 'Ab'
    if (d_Gb <= dmax):
        dickey['Gbm'] = 'Gb'
        dickey['A'] = 'A'
    if (d_G <= dmax):
        dickey['Gm'] = 'G'
        dickey['Bb'] = 'Bb'
    
    if (dickey == X):
        dickey['Desconocido'] = 'No se pudo determinar'
        
    return dickey

def obtenerKey(energy, dmax):
    # Guardamos la suma de las energías de cada pitch en un diccionario 
    # con los notas como identificador, y un identificador 'Nulo': 0
    pitches = {'C': 0, 'Db': 0, 'D': 0, 'Eb': 0, 'E': 0,
                'F': 0, 'Gb': 0, 'G': 0, 'Ab': 0, 'A': 0,
                'Bb': 0, 'B': 0, 'Nulo': 0}
    pitches['C'] = sum(energy[0])
    pitches['Db'] = sum(energy[1])
    pitches['D'] = sum(energy[2])
    pitches['Eb'] = sum(energy[3])
    pitches['E'] = sum(energy[4])
    pitches['F'] = sum(energy[5])
    pitches['Gb'] = sum(energy[6])
    pitches['G'] = sum(energy[7])
    pitches['Ab'] = sum(energy[8])
    pitches['A'] = sum(energy[9])
    pitches['Bb'] = sum(energy[10])
    pitches['B'] = sum(energy[11])
    
    # Llamamos a la funcion que determina la armadura
    string_pitches = determinarArmadura(pitches)
    
    
    # Generamos un diccionario de key con el identificador 'Nulo'
    dickey = {'Cm': 'Nulo', 'Dbm': 'Nulo', 'Dm': 'Nulo', 'Ebm': 'Nulo', 'Em': 'Nulo',
               'Fm': 'Nulo', 'Gbm': 'Nulo', 'Gm': 'Nulo', 'Abm': 'Nulo', 'Am': 'Nulo',
               'Bbm': 'Nulo', 'Bm': 'Nulo', 'C': 'Nulo', 'Db': 'Nulo', 'D': 'Nulo',
               'Eb': 'Nulo', 'E': 'Nulo', 'F': 'Nulo', 'Gb': 'Nulo', 'G': 'Nulo',
               'Ab': 'Nulo', 'A': 'Nulo', 'Bb': 'Nulo', 'B': 'Nulo', 'Desconocido': 'Nulo'}
    
    # Llamamos a la funcion comparar armadura, que nos devueleve la tonalidad
    # que se ajusta mejor a nuestra armadura
    
    # Comparamos el string obtenido con el correspondiente a
    # cierta tonalidad, y medimos su distancia de Levenshtein.
    
    dickey = compararKey(string_pitches, dmax, dickey)
    
    if (dickey['Desconocido'] == 'No se pudo determinar'):
        key = dickey['Desconocido']
        return key
      
    # Ya que es posible tener mas de una tonalidad con la misma distacia
    # de Levenshtein, revisamos cual es la nota dominante con la funcion dominante
    
    pkey = dominante(pitches, dickey)
        
    # Averiguamos cual es la key maxima y la asignamos a self.key
    
    key = max(pkey, key = pkey.get)
    
    return key

def asignarCamelotValue(keySong):
    camelotkey = [None, '']
    if (keySong == 'Abm'):
        camelotkey[0] = 1
        camelotkey[1] = 'A'
    elif (keySong == 'Ebm'):
        camelotkey[0] = 2
        camelotkey[1] = 'A'
    elif (keySong == 'Bbm'):
        camelotkey[0] = 3
        camelotkey[1] = 'A'
    elif (keySong == 'Fm'):
        camelotkey[0] = 4
        camelotkey[1] = 'A'
    elif (keySong == 'Cm'):
        camelotkey[0] = 5
        camelotkey[1] = 'A'
    elif (keySong == 'Gm'):
        camelotkey[0] = 6
        camelotkey[1] = 'A'
    elif (keySong == 'Dm'):
        camelotkey[0] = 7
        camelotkey[1] = 'A'
    elif (keySong == 'Am'):
        camelotkey[0] = 8
        camelotkey[1] = 'A'
    elif (keySong == 'Em'):
        camelotkey[0] = 9
        camelotkey[1] = 'A'
    elif (keySong == 'Bm'):
        camelotkey[0] = 10
        camelotkey[1] = 'A'
    elif (keySong == 'Bm'):
        camelotkey[0] = 11
        camelotkey[1] = 'A'
    elif (keySong == 'Gbm'):
        camelotkey[0] = 12
        camelotkey[1] = 'A'
    if (keySong == 'B'):
        camelotkey[0] = 1
        camelotkey[1] = 'B'
    elif (keySong == 'Gb'):
        camelotkey[0] = 2
        camelotkey[1] = 'B'
    elif (keySong == 'Db'):
        camelotkey[0] = 3
        camelotkey[1] = 'B'
    elif (keySong == 'Ab'):
        camelotkey[0] = 4
        camelotkey[1] = 'B'
    elif (keySong == 'Eb'):
        camelotkey[0] = 5
        camelotkey[1] = 'B'
    elif (keySong == 'Bb'):
        camelotkey[0] = 6
        camelotkey[1] = 'B'
    elif (keySong == 'F'):
        camelotkey[0] = 7
        camelotkey[1] = 'B'
    elif (keySong == 'C'):
        camelotkey[0] = 8
        camelotkey[1] = 'B'
    elif (keySong == 'G'):
        camelotkey[0] = 9
        camelotkey[1] = 'B'
    elif (keySong == 'D'):
        camelotkey[0] = 10
        camelotkey[1] = 'B'
    elif (keySong == 'A'):
        camelotkey[0] = 11
        camelotkey[1] = 'B'
    elif (keySong == 'E'):
        camelotkey[0] = 12
        camelotkey[1] = 'B'
    
    return camelotkey