from reproductor import Reproductor
from mpv import MPV, MpvEvent


class ReproductorNativo(Reproductor):

    def __init__(self, lista_videos: list[str]) -> None:
        self._reproductor = MPV(
            ytdl=True,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True
        )
        self._reproductor.fullscreen = True

        self._video_actual = [ 0 ]
        self._velocidades_disponibles = [ 1, 1.5, 2 ]
        self._velocidad_actual = [ 0 ]
        self._cooldown_acciones = {
            'PausaReproduccion'     : [0, 1500],
            'AvanceRetroceso'       : [0, 500],
            'AnteriorSiguiente'     : [0, 1500],
            'Velocidad'             : [0, 1000]
        }

        self._longitud_lista_reproduccion = len(lista_videos)
        for video in lista_videos:
            self._reproductor.playlist_append(video)


    def comenzar_reproduccion(self, terminar_reproduccion: callable) -> None:
        @self._reproductor.event_callback('shutdown')
        def finalizar_reproduccion_cierre_manual(evento):
            terminar_reproduccion()

        @self._reproductor.event_callback('end_file')
        def finalizar_reproduccion_fin_video(evento: MpvEvent):
            if evento.as_dict()['reason'] == b'eof' and evento.as_dict()['playlist_entry_id'] == self._longitud_lista_reproduccion:
                terminar_reproduccion()

        self._reproductor.playlist_play_index(0)
        print(f'Reproduciendo {self._reproductor.playlist_filenames[self._video_actual[0]]}')


    def pausar_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            self._reproductor._set_property('pause', True)
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción pausada')


    def renaudar_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            self._reproductor._set_property('pause', False)
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción renaudada')


    def alternar_pausa_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            self._reproductor._set_property('pause', not self._reproductor._get_property('pause'))
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción pausada') if self._reproductor._get_property('pause') else \
                print('Reproducción renaudada')
    

    def saltar_hacia_delante(self, marca_de_tiempo: int=0, cantidad: int=5) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AvanceRetroceso'][0] > self._cooldown_acciones['AvanceRetroceso'][1]:
            self._reproductor.seek(amount=cantidad, reference='relative')
            self._cooldown_acciones['AvanceRetroceso'][0] = marca_de_tiempo
            print(f'Salto de {cantidad} segundos')


    def saltar_hacia_atras(self, marca_de_tiempo: int=0, cantidad: int=5) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AvanceRetroceso'][0] > self._cooldown_acciones['AvanceRetroceso'][1]:
            self._reproductor.seek(amount=-cantidad, reference='relative')
            self._cooldown_acciones['AvanceRetroceso'][0] = marca_de_tiempo
            print(f'Retroceso de {cantidad} segundos')
    

    def reproducir_siguiente(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AnteriorSiguiente'][0] > self._cooldown_acciones['AnteriorSiguiente'][1]:
            if self._video_actual[0] + 1 < self._longitud_lista_reproduccion:
                self._reproductor.playlist_next()
                self._cooldown_acciones['AnteriorSiguiente'][0] = marca_de_tiempo
                self._video_actual[0] += 1
                print(f'Reproduciendo siguiente video: {self._reproductor.playlist_filenames[self._video_actual[0]]}')


    def reproducir_anterior(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AnteriorSiguiente'][0] > self._cooldown_acciones['AnteriorSiguiente'][1]:
            if self._video_actual[0] - 1 >= 0:
                self._reproductor.playlist_prev()
                self._cooldown_acciones['AnteriorSiguiente'][0] = marca_de_tiempo
                self._video_actual[0] -= 1
                print(f'Reproduciendo video anterior: {self._reproductor.playlist_filenames[self._video_actual[0]]}')
    

    def aumentar_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            if self._velocidad_actual[0] + 1 < len(self._velocidades_disponibles):
                self._velocidad_actual[0] += 1
                self._reproductor._set_property('speed', self._velocidades_disponibles[self._velocidad_actual[0]])
                self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
                print(f'Aumentando velocidad a {self._velocidades_disponibles[self._velocidad_actual[0]]}')


    def disminuir_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            if self._velocidad_actual[0] - 1 >= 0:
                self._velocidad_actual[0] -= 1
                self._reproductor._set_property('speed', self._velocidades_disponibles[self._velocidad_actual[0]])
                self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
                print(f'Disminuyendo velocidad a {self._velocidades_disponibles[self._velocidad_actual[0]]}')


    def cambiar_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            self._velocidad_actual[0] = (self._velocidad_actual[0] + 1) % len(self._velocidades_disponibles)
            self._reproductor._set_property('speed', self._velocidades_disponibles[self._velocidad_actual[0]])
            self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
            print(f'Cambiando velocidad a {self._velocidades_disponibles[self._velocidad_actual[0]]}')


    def cerrar_reproductor(self) -> None:
        self._reproductor.stop()