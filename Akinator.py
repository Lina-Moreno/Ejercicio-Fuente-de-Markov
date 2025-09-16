# Probabilidades de ocurrencia de las letras en español (porcentaje)
# Se basa en una aproximación puede mejorar con un gran archivo de texto en español y calcaulando las probabilidades
# para cada letra. 
prob_letras = {
    'a': 11.96, 'e': 14.53, 'o': 8.68, 's': 7.84, 'i': 7.64,
    'l': 7.23, 'r': 6.87, 'n': 6.83, 'd': 4.96, 'u': 4.79,
    't': 4.19, 'c': 3.42, 'p': 2.76, 'm': 2.65, 'y': 2.37,
    'g': 1.13, 'b': 1.05, 'h': 0.96, 'q': 0.90, 'f': 0.70,
    'v': 0.61, 'j': 0.52, 'ñ': 0.31, 'z': 0.28, 'x': 0.20,
    'k': 0.12, 'w': 0.04
}

# Cadena de Markov de primer orden (probabilidades de transición)
# Un diccionario anidado: {'letra_anterior': {'siguiente_letra': probabilidad}}
# Estos datos son una simplificación para el ejemplo, si queremos que el programa sea "más inteligente" tendriamos que
# analizar más datos con un gran archivo de texto en español por ejemplo. 
# esto para optener todas las posibles combinaciones de letras con sus probabilidades.
transicion_letras = {
    'a': {'l': 0.2, 's': 0.15, 'c': 0.1, 'n': 0.1, 'r': 0.1, 'd': 0.05, 'g': 0.05},
    'e': {'s': 0.2, 'r': 0.15, 'l': 0.1, 'd': 0.1, 'c': 0.05, 't': 0.05, 'n': 0.05},
    'i': {'n': 0.2, 'c': 0.15, 's': 0.1, 'd': 0.1, 'r': 0.05, 'm': 0.05},
    'o': {'s': 0.2, 'n': 0.15, 'l': 0.1, 'c': 0.1, 'r': 0.05, 'm': 0.05},
    'u': {'e': 0.8, 'n': 0.1, 'i': 0.1},
    'c': {'a': 0.4, 'o': 0.3, 'e': 0.2, 'u': 0.1},
    'q': {'u': 1.0},
    's': {'e': 0.4, 'a': 0.3, 'o': 0.2, 'i': 0.1},
    'ñ': {'a': 0.5, 'e': 0.3, 'o': 0.2},
    'p': {'a': 0.5, 'o': 0.3, 'e': 0.2},
    't': {'a': 0.6, 'e': 0.3, 'o': 0.1},
    'l': {'a': 0.5, 'o': 0.3, 'e': 0.2},
    'm': {'a': 0.4, 'e': 0.3, 'o': 0.2, 'i': 0.1}
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
                        if letra not in letras_adivinadas and prob > mejor_prob:
                            mejor_prob = prob
                            mejor_letra = letra
    
    # Si no se puede usar Markov, usamos la probabilidad general más alta.
    if mejor_letra is None:
        letras_disponibles = [letra for letra in prob_letras.keys() if letra not in letras_adivinadas]
        if letras_disponibles:
            mejor_letra = sorted(letras_disponibles, key=lambda l: prob_letras[l], reverse=True)[0]
    
    return mejor_letra


def adivinar_ahorcado():
    print("¡Piensa en una palabra de 4 letras! Yo intentaré adivinarla.")
    
    patron = ["_"] * 4
    letras_adivinadas = set()
    intentos = 0
    
    # Aquí es donde cambias el número máximo de intentos
    while "_" in patron and intentos < 25:
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