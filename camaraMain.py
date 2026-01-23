import flet as ft
import threading
import time
from camara import EscanerSeguridad

class CamaraMain(ft.Container):
    def __init__(self,indice, label_name="Sector", onclick=None, Grid:bool=False):
        super().__init__(
            on_click=onclick,
            data=indice,
            ink=True
        )
        self.stop_event = threading.Event()
        self.is_running = False
        self.indice = indice
        self.label_name = label_name
        self.Grid=Grid
        self.frame_count = 0  # Contador para saltar frames
        self.mouse_cursor = ft.MouseCursor.PRECISE # 2. Cursor de "manito" al pasar el mouse
        
        # UI inicial
        self.feed = ft.Image(
            src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
            fit=ft.ImageFit.CONTAIN,
            border_radius = 50,
            expand=True
        )
        self.text_counter = ft.Text("Iniciando cámara...", size=25,bgcolor=ft.Colors.GREEN,weight="bold")
        
        self.content = ft.Column([
            ft.Text(f"Camara", weight="bold"),
            self.feed,
            self.text_counter
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        self.IniHilo()

    def IniHilo(self):
        print('inicio') # <--- Flet lo llama automáticamente cuando se agrega a la página
        self.stop_event.clear()
        self.is_running = True
        self.camara_logic = EscanerSeguridad(self.indice) # Se inicia al montar
        self.thread = threading.Thread(target=self.update_video, daemon=True)
        self.thread.start()

    def will_unmount(self):
        print('fin') # <--- Flet lo llama automáticamente al quitarlo
        self.stop_event.set()
        if hasattr(self, 'camara_logic'):
            self.camara_logic.liberar()

    def update_video(self):
        ultima_deteccion_texto = "Esperando..."
        
        while self.is_running and not self.stop_event.is_set():
            try:
                self.frame_count += 1
                img_b64 = None
                
                # --- ESTRATEGIA HÍBRIDA ---
                # Procesar IA solo cada 3 frames (ajusta este número según tu PC)
                # Si lo pones en 1, procesa todos. Si lo pones en 5, procesa 1 de cada 5.
                PROCESAR_IA = (self.frame_count % 3 == 0) 

                if PROCESAR_IA:
                    # Llamamos a la lógica pesada (YOLO)
                    resultado = None
                    if self.Grid:
                        resultado = self.camara_logic.inicio()
                    else:   
                        resultado = self.camara_logic.inicio2()
                    
                    if isinstance(resultado, tuple):
                        img_b64, results = resultado
                        # Actualizamos el contador solo cuando hay detección nueva
                        cant = len(results[0].boxes) if results else 0
                        ultima_deteccion_texto = f"Detecciones: {cant}"
                else:
                    # Llamamos a la lógica ligera (Solo imagen)
                    # NOTA: Debes haber agregado el método 'obtener_frame_solo' en camara.py
                    # Si no quieres editar camara.py, tendrás que asumir el lag o duplicar código aquí.
                    # Asumiendo que agregaste el método:
                    img_b64 = self.camara_logic.obtener_frame_solo()

                # --- ACTUALIZACIÓN DE UI ---
                if img_b64:
                    self.feed.src_base64 = img_b64
                    self.text_counter.value = ultima_deteccion_texto
                    
                    if not self.stop_event.is_set():
                        self.update() 
                
                # Un sleep minúsculo para no quemar el CPU en bucles vacíos, 
                # pero mucho menor que antes.
                time.sleep(0.005) 

            except RuntimeError as e:
                if "Event loop is closed" in str(e):
                    self.is_running = False
                    break
            except Exception as e:
                print(f"Error en cámara {self.indice}: {e}")

    def setIndice(self, nuevo_indice):
        # 1. Pausar lectura
        self.stop_event.set()

        # 2. Esperar al hilo
        if self.thread.is_alive():
            self.thread.join()

        # 3. Actualizar índice
        self.indice = nuevo_indice
        self.data = nuevo_indice
        self.frame_count = 0

        # 4. Cambiar cámara de forma segura
        self.camara_logic.cambiar_camara(nuevo_indice)

        # 5. Reiniciar loop
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.update_video, daemon=True)
        self.thread.start()
   

    def liberar_recursos(self):
        self.stop_event.set()
        self.thread.join()
        if hasattr(self, 'camara_logic'):
            self.camara_logic.liberar()
    def get_indice(self):
        return self.indice
