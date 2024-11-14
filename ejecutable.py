from clases import Detector, Radiacion, Virus, Sanador  # Importación de las clases necesarias

def main():
    matriz = []
    print("Ingrese la matriz de ADN de 6x6 usando solo caracteres A, G, T y C:")

    # Recolección de la matriz de ADN, verificando que cada fila cumpla con el formato
    for i in range(6):
        while True:
            Adn = input(f"Fila {i+1}/6: ").upper()
            if len(Adn) == 6 and all(letra in {'A', 'G', 'T', 'C'} for letra in Adn):
                matriz.append(Adn)
                break
            else:
                print("Error: La cadena debe tener exactamente 6 letras y solo letras A, G, T o C.")

    detector = Detector()
    sanador = Sanador()

    print("\nADN original:")
    for fila in matriz:
        print(fila)

    while True:
        try:
            # Menú de opciones
            opcion = int(input("\n¿Qué deseas hacer? (1: Detectar mutantes, 2: Mutar, 3: Sanar, 4: Salir): "))
            
            if opcion == 1:
                # Detectar mutantes y mostrar el resultado
                mutante_detectado = detector.detectar_mutantes(matriz)
                print("Se detectó un mutante en el ADN." if mutante_detectado else "No se detectaron mutantes.")

            elif opcion == 2:
                # Selección de tipo de mutación
                tipo_mutacion = ""
                while tipo_mutacion not in ['H', 'V', 'D']:
                    tipo_mutacion = input("¿Deseas mutar con radiación horizontal (H), vertical (V) o virus (D)? ").upper()
                
                # Selección de la base nitrogenada a mutar
                adn = ""
                while adn not in ["A", "G", "T", "C"]:
                    adn = input("¿Qué ADN deseas cambiar (A, G, T, C)?: ").upper()

                # Crear el mutante según la opción seleccionada
                if tipo_mutacion in ['H', 'V']:
                    radiacion = Radiacion(adn)
                    nueva_matriz = radiacion.crear_mutante(matriz, (1, 0), tipo_mutacion)
                elif tipo_mutacion == 'D':
                    virus = Virus(adn)
                    nueva_matriz = virus.crear_mutante(matriz, (0, 0))

                # Mostrar la matriz mutada
                print("ADN mutado:")
                for fila in nueva_matriz:
                    print(fila)
                matriz = nueva_matriz  # Actualiza la matriz original

            elif opcion == 3:
                # Sanar el ADN y mostrar el resultado
                nueva_matriz = sanador.sanar_mutantes(matriz, detector)
                print("ADN sanado:")
                for fila in nueva_matriz:
                    print(fila)
                matriz = nueva_matriz  # Actualiza la matriz original

            elif opcion == 4:
                print("Salió del programa con éxito.")
                break  # Salir del bucle

            else:
                print("Opción inválida, por favor selecciona nuevamente.")

        except ValueError:
            print("Entrada inválida. Por favor ingresa un número.")

if __name__ == "__main__":
    main()
