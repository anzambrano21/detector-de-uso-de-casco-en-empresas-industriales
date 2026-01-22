import flet as ft
import os

from camaraMain import CamaraMain 


# Fix para el error de loop de eventos en Windows
if os.name == 'nt':
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
        return wrapper
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Escaneo de seguridad del personal"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Dimensiones iniciales (ajustadas para ver las cámaras)
    page.window.width = 1500 
    page.window.height = 800
    page.window.resizable = True  # Recomendado para ver múltiples cámaras
    
    # Definimos los índices de las cámaras que queremos abrir
    # Puedes usar [0] para una sola o [0, 1] si tienes dos
    indices_camaras = [1] 


    def change_main_camera(e):
        
        nueva_indice = panel_CamaraPrincipal.get_indice()
        indice_click = e.control.get_indice()
        print(f'registro click en camara {indice_click}, intercambiando con camara {nueva_indice}')
        # 1. Liberar recursos de AMBAS cámaras antes de intercambiar.
        # Esto evita que OpenCV falle por intentar abrir una cámara que ya está en uso.
        panel_CamaraPrincipal.liberar_recursos()
        
        e.control.liberar_recursos()
        
        
        # Usamos get_indice() para asegurar que tenemos el valor actual, no el inicial
        
        panel_CamaraPrincipal.setIndice(indice_click)
        
        e.control.setIndice(nueva_indice)
        
        


    def camaras_component(page: ft.Page, lista_indices=[0],grid:bool=True):
        layout = ft.ResponsiveRow(
            controls=[
                # No hace falta meterlo en otro Container si CameraCard ya es un Container
                CamaraMain(indice=idx, label_name=f"Camara {i+1}", Grid=grid,onclick=change_main_camera)
                for i, idx in enumerate(lista_indices)
            ],
            spacing=20,
            run_spacing=20,
        )
        # Configuramos las columnas (breakpoints) para cada tarjeta
        for control in layout.controls:
            control.col = {"sm": 12, "md": 6, "lg": 4}
        return ft.Column([
            ft.Divider(height=10, color="transparent"),
            layout
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    

    # Contenido principal
    # Usamos una Column con scroll para que si hay muchas cámaras se pueda bajar
    panel_camaras = camaras_component(page, lista_indices=indices_camaras, grid=True)
    panel_CamaraPrincipal= CamaraMain(0,'camara Principal',Grid=False)
    panel_CamaraPrincipal.expand=6
    panel_camaras.expand=4


    page.add(ft.Row(controls=[
        panel_CamaraPrincipal,
        panel_camaras
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND, expand=True))

# Iniciar la aplicación
if __name__ == "__main__":
    ft.app(target=main)