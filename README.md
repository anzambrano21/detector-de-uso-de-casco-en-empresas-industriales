#  Detector de Uso de Casco en Empresas Industriales

![Estado](https://img.shields.io/badge/Estado-En_Desarrollo-orange)
![Python](https://img.shields.io/badge/Python-3.X-blue)


##  Descripción del Proyecto

Este sistema es un programa de vigilancia automatizada diseñado para **instalaciones petroleras**. Utilizando visión artificial, el software monitorea el video en tiempo real para verificar que todo el personal esté utilizando su **casco de seguridad**.

###  Objetivo
Prevenir accidentes laborales y asegurar el cumplimiento de las normas de seguridad (HSE) mediante alertas visuales inmediatas.

---

##  Funcionamiento de la Alerta

El sistema analiza cada cuadro de video y toma decisiones basadas en la detección del casco:

1.  ** Uso Correcto:** Si el operario tiene casco, el sistema continúa el monitoreo normal.
2.  ** FALTA DE CASCO (Alerta Roja):** Si se detecta a una persona sin el equipo de protección, **la imagen se torna roja** y se muestra una advertencia visual clara para el guardia de seguridad.


##  Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Visión por Computadora:** OpenCV
* **IA / Detección:** YOLO 
* **Interfaz:** Flutter

---

##  Instalación y Uso

Sigue estos pasos para probar el detector en tu computadora:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/detector-casco-industrial.git](https://github.com/tu-usuario/detector-casco-industrial.git)
    ```
2.  **Ejecutar el programa:**
    ```bash
    python main.py
    ```

---

