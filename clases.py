class Detector:
    def __init__(self)->None:
        self.matriz = []
        """Clase para detectar mutantes en una matriz de ADN."""

    def detectar_mutantes(self, matriz: list)->bool:
        # Guarda la matriz y verifica si hay mutantes en cualquier dirección
        self.matriz = matriz
        if self._detectar_horizontal() or self._detectar_vertical() or self._detectar_diagonal():
            return True
        return False

    def _detectar_horizontal(self)->bool:
        # Revisa cada fila de la matriz en busca de secuencias mutantes horizontales
        for fila in self.matriz:
            if self._repeticion(fila):
                return True
        return False

    def _detectar_vertical(self)->bool:
        # Revisa cada columna de la matriz en busca de secuencias mutantes verticales
        for columna in range(len(self.matriz[0])):
            secuencia = ''.join([self.matriz[fila][columna] for fila in range(len(self.matriz))])
            if self._repeticion(secuencia):
                return True
        return False

    def _detectar_diagonal(self)->bool:
        # Revisa diagonales en busca de secuencias mutantes
        n = len(self.matriz)
        for i in range(n-3):
            for j in range(n-3):
                diagonal_principal = ''.join([self.matriz[i+k][j+k] for k in range(4)])
                diagonal_secundaria = ''.join([self.matriz[i+k][j+3-k] for k in range(4)])
                if self._repeticion(diagonal_principal) or self._repeticion(diagonal_secundaria):
                    return True
        return False

    def _repeticion(self, secuencia)->bool:
        # Verifica si hay cuatro letras idénticas consecutivas
        for i in range(len(secuencia) - 3):
            if secuencia[i:i+4] == secuencia[i] * 4:
                return True
        return False


# Clase Mutador: clase base para mutaciones de ADN
class Mutador:
    def __init__(self, base_nitrogenada)->None:
        self.base_nitrogenada = base_nitrogenada

    def crear_mutante(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")


# Clase Radiacion: genera mutaciones horizontales o verticales
class Radiacion(Mutador):
    def __init__(self, base_nitrogenada)->None:
        super().__init__(base_nitrogenada)

    def crear_mutante(self, matriz:list, posicion_inicial, orientacion_de_la_mutacion)->bool:
        # Intenta crear una mutación en la matriz según la orientación
        try:
            fila, columna = posicion_inicial
            if orientacion_de_la_mutacion == 'H':
                # Reemplaza cuatro bases consecutivas horizontalmente
                matriz[fila] = matriz[fila][:columna] + self.base_nitrogenada * 4 + matriz[fila][columna+4:]
            elif orientacion_de_la_mutacion == 'V':
                # Reemplaza cuatro bases consecutivas verticalmente
                for i in range(4):
                    matriz[fila + i] = matriz[fila + i][:columna] + self.base_nitrogenada + matriz[fila + i][columna + 1:]
            return matriz
        except Exception as e:
            print(f"Error creando mutante: {e}")
            return None


# Clase Virus: genera mutaciones diagonales en la matriz
class Virus(Mutador):
    def __init__(self, base_nitrogenada)->None:
        super().__init__(base_nitrogenada)

    def crear_mutante(self, matriz:list, posicion_inicial)->bool:
        # Intenta crear una mutación en diagonal
        try: 
            fila, columna = posicion_inicial
            for i in range(4):
                matriz[fila + i] = matriz[fila + i][:columna + i] + self.base_nitrogenada + matriz[fila + i][columna + i + 1:]
            return matriz
        except Exception as e:
            print(f"Error creando mutante: {e}")
            return None


# Clase Sanador: sana el ADN generando una nueva matriz sin mutantes

class Sanador:
    def __init__(self)->None:
        pass
    
    def sanar_mutantes(self, matriz: list, detector)->bool:
        # Si se detecta un mutante, genera un ADN sin mutaciones
        nueva_matriz = self._generar_adn_no_mutante(len(matriz), detector)
        return nueva_matriz

    def _generar_adn_no_mutante(self, n, detector)->bool:
        import random
        bases = ['A', 'T', 'C', 'G']

        def generar_fila_sin_mutacion()->bool:
            while True:
                fila = ''.join(random.choice(bases) for _ in range(n))
                # Verifica secuencias horizontales de cuatro bases consecutivas
                if not any(fila[i] == fila[i+1] == fila[i+2] == fila[i+3] for i in range(n - 3)):
                    return fila

        # Genera la matriz completa
        while True:
            nueva_matriz = [generar_fila_sin_mutacion() for _ in range(n)]
            # Usa el detector para verificar si la matriz generada tiene mutaciones
            if not detector.detectar_mutantes(nueva_matriz):
                return nueva_matriz  # Retorna solo si no hay mutantes
