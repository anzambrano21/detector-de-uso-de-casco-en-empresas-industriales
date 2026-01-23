import time
import cv2
import torch
from ultralytics import YOLO
import math
import base64
import os
MODELO_YOLO = YOLO(r'C:\Users\Angel\runs\detect\train4\weights\best.pt')
class EscanerSeguridad:
    def __init__(self,indice):
        # Inicializar la cámara una sola vez al crear el objeto
        self.__camara = cv2.VideoCapture(indice,cv2.CAP_DSHOW)
        
        # Intentar cargar el modelo entrenado (best.pt), si no existe, usa el base (yolov8n.pt)
        # Nota: La ruta 'runs/detect/train/weights/best.pt' se crea tras ejecutar entrenar_modelo.py
        self.model = MODELO_YOLO
    def inicio(self):
        # Verificar si la cámara está abierta
        if not self.__camara.isOpened():
            return ""

        self.busqueda, self.imagen = self.__camara.read()
        if not self.busqueda:
            return ""

        self.imagen=cv2.resize(self.imagen, (640, 480))
        self.imagen = cv2.flip(self.imagen, 1)
        
        # Realizar la detección con YOLO
        # conf=0.5 descarta detecciones con menos del 50% de probabilidad
        results = self.model(self.imagen, verbose=False, conf=0.5)
               

        _, buffer = cv2.imencode('.jpg', self.imagen)
        # Convertir el búfer (bytes JPEG) a una cadena Base64
        imagen_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return imagen_base64 ,results
    def inicio2(self):
        
            # Verificar si la cámara está abierta
            if not self.__camara.isOpened():
                return ""

            self.busqueda, self.imagen = self.__camara.read()
            if not self.busqueda:
                return ""

            self.imagen=cv2.resize(self.imagen, (640, 480))
            self.imagen = cv2.flip(self.imagen, 1)
            
            # Realizar la detección con YOLO
            # conf=0.5 descarta detecciones con menos del 50% de probabilidad
            results = self.model.predict(
                                            self.imagen,
                                            conf=0.5,
                                            imgsz=416,
                                            device="cuda" if torch.cuda.is_available() else "cpu",
                                            verbose=False
                                        )
            
            # Iterar sobre los resultados para diferenciar etiquetas
           
                    

            # Dibujar las cajas delimitadoras y etiquetas en la imagen
            self.imagen = results[0].plot()
            

            _, buffer = cv2.imencode('.jpg', self.imagen)
            # Convertir el búfer (bytes JPEG) a una cadena Base64
            imagen_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return imagen_base64 ,results

    def liberar(self):
        if self.__camara.isOpened():
            self.__camara.release()
            
    def obtener_frame_solo(self):
        """Obtiene el frame, lo redimensiona y devuelve en base64 SIN pasar por YOLO"""
        if not self.__camara.isOpened():
            return None
        
        ret, frame = self.__camara.read()
        if not ret:
            return None

        # Mismo pre-procesamiento visual
        frame = cv2.resize(frame, (256, 192))
        frame = cv2.flip(frame, 1)

        _, buffer = cv2.imencode('.jpg', frame)
        imagen_base64 = base64.b64encode(buffer).decode('utf-8')
        return imagen_base64
    def cambiar_camara(self, nuevo_indice):
        try:
                if self.__camara.isOpened():
                    self.__camara.release()

                time.sleep(0.3)  # IMPORTANTE para drivers Windows

                self.__camara = cv2.VideoCapture(nuevo_indice, cv2.CAP_DSHOW)

                if not self.__camara.isOpened():
                    print("⚠️ No se pudo abrir la cámara", nuevo_indice)

        except Exception as e:
                print("❌ ERROR CRÍTICO CÁMARA:", e)