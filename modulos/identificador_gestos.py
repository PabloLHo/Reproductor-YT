import os
from cv2 import VideoCapture, flip, destroyAllWindows, imshow, waitKey
from time import time
import mediapipe as mp
from reproductor import Reproductor
from utils import silenciar_salida


class IdentificadorGestos:

    def __init__(self, reproductor: Reproductor) -> None:
        self._camara = VideoCapture(0)

        self._reproductor = reproductor

        self._terminar_identificacion = [ None ]
        self._condicion_finalizacion = [ True ]

        # Configurar identificadores
        configuracion_modelo_nativo = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=os.path.abspath('.\\modelos_identificacion_gestos\\modelo_nativo.task')),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            min_hand_detection_confidence = 0.3, 
            min_hand_presence_confidence = 0.3, 
            min_tracking_confidence = 0.3, 
            result_callback=self._procesar_resultado_modelo_nativo
        )

        configuracion_modelo_personalizado = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=os.path.abspath('.\\modelos_identificacion_gestos\\modelo_personalizado.task')),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            min_hand_detection_confidence = 0.3, 
            min_hand_presence_confidence = 0.3, 
            min_tracking_confidence = 0.3, 
            result_callback=self._procesar_resultado_modelo_personalizado
        )

        with silenciar_salida():
            self._identificador_gestos_nativo = mp.tasks.vision.GestureRecognizer.create_from_options(configuracion_modelo_nativo)
            self._identificador_gestos_personalizado = mp.tasks.vision.GestureRecognizer.create_from_options(configuracion_modelo_personalizado)
    

    def _procesar_resultado_modelo_nativo(self, resultado, salida, timestamp) -> None:
        if resultado.gestures:
            gesto = resultado.gestures[0][0].category_name
            if gesto == 'Thumb_Up':
                self._reproductor.saltar_hacia_delante(timestamp)
            elif gesto == 'Open_Palm':
                self._reproductor.alternar_pausa_reproduccion(timestamp)
            elif gesto == 'Pointing_Up':
                self._reproductor.cambiar_velocidad(timestamp)
            elif gesto == 'Victory':
                self._reproductor.reproducir_siguiente(timestamp)
            elif gesto == 'Thumb_Down':
                self._reproductor.saltar_hacia_atras(timestamp)
    

    def _procesar_resultado_modelo_personalizado(self, resultado, salida, timestamp) -> None:
        if resultado.gestures:
            gesto = resultado.gestures[0][0].category_name
            if gesto == 'Rock':
                self._reproductor.reproducir_anterior(timestamp)
            elif gesto == 'Ok':
                if self._terminar_identificacion[0]:
                    self._terminar_identificacion[0]()
            else:
                self._identificador_gestos_nativo.recognize_async(image=salida, timestamp_ms=timestamp)
    

    def comenzar_identificacion(self, callback_finalizacion: callable):
        self._terminar_identificacion[0] = callback_finalizacion
        self._condicion_finalizacion[0] = False 
        while not self._condicion_finalizacion[0]:
            ret, frame = self._camara.read()
            frame = flip(frame, 1)
            imshow('Video', frame)
            marca_de_tiempo = int(time() * 1000)
            mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB,
                                data=frame)
            try:
                self._identificador_gestos_personalizado.recognize_async(
                    image=mp_frame, timestamp_ms=marca_de_tiempo
                )
                if waitKey(1) & 0xFF == 27:
                    break
            except:
                pass

        self._terminar_identificacion[0] = None
        self._camara.release()
        destroyAllWindows()


    def finalizar_identificacion(self):
        self._condicion_finalizacion[0] = True