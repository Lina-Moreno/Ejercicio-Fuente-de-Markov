#Probabilidad de frecuencia de letras en español
prob_letras = {
    'a': 0.1196, 'b': 0.0092, 'c': 0.0292, 'd': 0.0687, 'e': 0.1678,
    'f': 0.0052, 'g': 0.0073, 'h': 0.0089, 'i': 0.0415, 'j': 0.0030,
    'k': 0.0001, 'l': 0.0837, 'm': 0.0212, 'n': 0.0701, 'ñ': 0.0029,
    'o': 0.0869, 'p': 0.0276, 'q': 0.0153, 'r': 0.0494, 's': 0.0788,
    't': 0.0331, 'u': 0.0480, 'v': 0.0039, 'w': 0.0001, 'x': 0.0006,
    'y': 0.0154, 'z': 0.0015
}

#Probabilidad letra inicial de una palabra de 4 letras
prob_inicio = {
    'a': 0.12, 'b': 0.08, 'c': 0.12, 'd': 0.08, 'e': 0.06, 
    'f': 0.04, 'g': 0.03, 'h': 0.03, 'i': 0.02, 'j': 0.02,
    'l': 0.08, 'm': 0.10, 'n': 0.06, 'o': 0.04, 'p': 0.08,
    'r': 0.06, 's': 0.08, 't': 0.08, 'u': 0.02, 'v': 0.04   
}

#Probabilidad letra final en una palabra de 4 letras
prob_final = {
    'a': 0.28, 'e': 0.15, 'o': 0.25, 's': 0.18, 'r': 0.08,  
    'n': 0.04, 't': 0.02                                  
}

# Diccionario anidado para representar cadena de Markov de primer orden
transicion_letras = {
    'a': {'r': 0.25, 'n': 0.20, 'd': 0.15, 's': 0.15, 'l': 0.12, 'c': 0.08, 'm': 0.05},
    'b': {'a': 0.40, 'e': 0.25, 'i': 0.20, 'o': 0.15},
    'c': {'a': 0.35, 'o': 0.30, 'e': 0.20, 'i': 0.15},
    'd': {'a': 0.30, 'e': 0.35, 'o': 0.25, 'i': 0.10},
    'e': {'s': 0.25, 'n': 0.20, 'r': 0.20, 't': 0.15, 'l': 0.12, 'm': 0.08},
    'f': {'a': 0.30, 'e': 0.25, 'i': 0.25, 'o': 0.20},
    'g': {'a': 0.40, 'o': 0.30, 'u': 0.30},
    'h': {'a': 0.50, 'o': 0.30, 'i': 0.20},
    'i': {'n': 0.25, 's': 0.20, 'r': 0.15, 'd': 0.15, 'c': 0.12, 't': 0.10, 'v': 0.03},
    'j': {'a': 0.50, 'o': 0.30, 'u': 0.20},
    'l': {'a': 0.35, 'e': 0.25, 'o': 0.20, 'i': 0.15, 'u': 0.05},
    'm': {'a': 0.35, 'e': 0.30, 'o': 0.20, 'i': 0.15},
    'n': {'a': 0.25, 'e': 0.20, 'o': 0.20, 'i': 0.15, 't': 0.15, 'd': 0.05},
    'o': {'r': 0.25, 's': 0.20, 'n': 0.18, 'c': 0.12, 't': 0.10, 'd': 0.08, 'm': 0.07},
    'p': {'a': 0.35, 'e': 0.25, 'o': 0.25, 'i': 0.15},
    'q': {'u': 1.0},
    'r': {'a': 0.30, 'e': 0.25, 'o': 0.20, 'i': 0.15, 'u': 0.10},
    's': {'a': 0.20, 'e': 0.20, 'o': 0.20, 'i': 0.15, 'u': 0.15, 't': 0.10},
    't': {'a': 0.30, 'e': 0.25, 'o': 0.25, 'i': 0.15, 'u': 0.05},
    'u': {'n': 0.25, 'r': 0.20, 's': 0.20, 'e': 0.15, 'l': 0.12, 'm': 0.08},
    'v': {'a': 0.40, 'e': 0.25, 'i': 0.20, 'o': 0.15}
}

# Función para obtener la mejor letra basándose en un patrón
def obtener_mejor_letra(patron, letras_adivinadas):
    
    if "_" not in patron:
        return None
    
    mejor_letra = None
    mejor_prob = -1
    
    # Intentar adivinar la siguiente letra basándose en la letra anterior (Markov)
    for i in range(len(patron)):
        if patron[i] == "_":
            if i > 0 and patron[i-1] != "_":
                letra_anterior = patron[i-1]
                if letra_anterior in transicion_letras:
                    for letra, prob in transicion_letras[letra_anterior].items():
                        if letra not in letras_adivinadas:
                            prob_ajustada = prob
                            if i == 3:  # última posición
                                prob_ajustada *= prob_final.get(letra, 0.3)
                            if prob_ajustada > mejor_prob:
                                mejor_prob = prob_ajustada
                                mejor_letra = letra
                if mejor_letra:
                    return mejor_letra
    
    # Si no se puede usar Markov, usamos la probabilidad general más alta.
    letras_disponibles = [l for l in prob_letras.keys() if l not in letras_adivinadas]
    for i in range(len(patron)):
        if patron[i] == "_":
            for letra in letras_disponibles:
                prob_base = prob_letras[letra]
                if i == 0:
                    prob_base *= prob_inicio.get(letra, 0.1)
                elif i == 3:
                    prob_base *= prob_final.get(letra, 0.1)
                if prob_base > mejor_prob:
                    mejor_prob = prob_base
                    mejor_letra = letra
                    
    return mejor_letra


def adivinar_ahorcado():
    print("¡Piensa en una palabra real de 4 letras en español! Yo intentaré adivinarla.")
    
    patron = ["_"] * 4
    letras_adivinadas = set()
    intentos = 0
    
    #Máximo de intentos
    while "_" in patron and intentos < 30:
        intentos += 1
        
        proxima_letra = obtener_mejor_letra(patron, letras_adivinadas)
        if proxima_letra is None:
            break
            
        letras_adivinadas.add(proxima_letra)
        
        print(f"\n--- Intento #{intentos} ---")
        print(f"Mi suposición es la letra: {proxima_letra.upper()}")
        
        respuesta = input(f"¿La palabra contiene la letra '{proxima_letra.upper()}'? (s/n): ").lower()
        
        if respuesta == 's':
            posiciones = input("¿En qué posiciones? (ej. 1,3): ")
            try:
                indices = [int(p.strip()) - 1 for p in posiciones.split(',')]
                for i in indices:
                    if 0 <= i < 4:
                        patron[i] = proxima_letra
                    else:
                        print("Posición fuera de rango. Intenta de nuevo.")
            except (ValueError, IndexError):
                print("Entrada inválida. Asegúrate de usar el formato '1,3'.")
                
            print(f"Patrón actual: {' '.join(patron)}")
            
        else:
            print("Ok, no está. Busco otra letra.")
            
    if "_" not in patron:
        print("\n¡He adivinado la palabra!")
        print(f"La palabra es: {''.join(patron).upper()}")
    else:
        print("\nMe he quedado sin intentos o la palabra es muy difícil para mí.")
        print(f"Lo que logré adivinar fue: {''.join(patron)}")

# Ejecutar el juego
adivinar_ahorcado()