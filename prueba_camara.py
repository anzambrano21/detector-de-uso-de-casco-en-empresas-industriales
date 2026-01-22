import cv2
from aplicacion.camara import EscanerSeguridad

def main():
    print("Inicializando cámara y modelo YOLO...")
    # Instanciar la clase
    escaner = EscanerSeguridad()
    
    print("Iniciando prueba. Presiona 'q' para salir.")
    
    try:
        while True:
            # Ejecutar el proceso de detección
            # inicio2 actualiza self.imagen internamente
            resultado = escaner.inicio2()
            
            if resultado == "":
                print("Error: No se pudo capturar imagen de la cámara.")
                break
            
            # Mostrar la imagen procesada (accediendo al atributo de la instancia)
            cv2.imshow("Prueba Escaner Seguridad", escaner.imagen)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        escaner.liberar()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()