from reproductor import Reproductor
from keyboard import press_and_release, press, release

ACCION = {
    'PausaReproduccion': 'k',
    'AVANCE':            'l',
    'RETROCESO':         'j'
}

class ReproductorYT(Reproductor):

    def __init__(self) -> None:
        self._estado_reproduccion = [ True ]
        self._video_actual = [ 0 ]
        self._velocidad_actual = [ 1.0 ]
        self._cooldown_acciones = {
            'PausaReproduccion'     : [0, 1500],
            'AvanceRetroceso'       : [0, 500],
            'AnteriorSiguiente'     : [0, 1500],
            'Velocidad'             : [0, 1000]
        }


    def comenzar_reproduccion(self, terminar_reproduccion: callable) -> None: print('Comenzando reproducción para Youtube.')
    def cerrar_reproductor(self) -> None: print('Cerrando la reproducción por Youtube.')


    def pausar_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            press_and_release(ACCION['PausaReproduccion'])
            self._estado_reproduccion[0] = False
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción pausada')


    def renaudar_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            press_and_release(ACCION['PausaReproduccion'])
            self._estado_reproduccion[0] = True
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción renaudada')


    def alternar_pausa_reproduccion(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['PausaReproduccion'][0] > self._cooldown_acciones['PausaReproduccion'][1]:
            press_and_release(ACCION['PausaReproduccion'])
            self._estado_reproduccion[0] = not self._estado_reproduccion[0]
            self._cooldown_acciones['PausaReproduccion'][0] = marca_de_tiempo
            print('Reproducción renaudada') if self._estado_reproduccion[0] else \
                print('Reproducción pausada')
    

    def saltar_hacia_delante(self, marca_de_tiempo: int=0, cantidad: int=10) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AvanceRetroceso'][0] > self._cooldown_acciones['AvanceRetroceso'][1]:
            for _ in range(int(cantidad / 10)): press_and_release(ACCION['AVANCE'])
            self._cooldown_acciones['AvanceRetroceso'][0] = marca_de_tiempo
            print(f'Salto de {cantidad} segundos')


    def saltar_hacia_atras(self, marca_de_tiempo: int=0, cantidad: int=10) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AvanceRetroceso'][0] > self._cooldown_acciones['AvanceRetroceso'][1]:
            for _ in range(int(cantidad / 10)): press_and_release(ACCION['RETROCESO'])
            self._cooldown_acciones['AvanceRetroceso'][0] = marca_de_tiempo
            print(f'Retroceso de {cantidad} segundos')
    

    def reproducir_siguiente(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AnteriorSiguiente'][0] > self._cooldown_acciones['AnteriorSiguiente'][1]:
            press_and_release('Shift+n')
            self._cooldown_acciones['AnteriorSiguiente'][0] = marca_de_tiempo
            print('Reproduciendo siguiente video')


    def reproducir_anterior(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['AnteriorSiguiente'][0] > self._cooldown_acciones['AnteriorSiguiente'][1]:
            press_and_release('Shift+p')
            self._cooldown_acciones['AnteriorSiguiente'][0] = marca_de_tiempo
            print('Reproduciendo video anterior')
    

    def aumentar_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            press_and_release('Shift+.')
            if self._velocidad_actual[0] < 2: self._velocidad_actual[0] += .25
            self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
            print(f'Aumentando velocidad a {self._velocidad_actual[0]}')


    def disminuir_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            press('Shift') ; press(',') ; release('Shift')
            if self._velocidad_actual[0] > .25: self._velocidad_actual[0] -= .25
            self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
            print(f'Disminuyendo velocidad a {self._velocidad_actual[0]}')


    def cambiar_velocidad(self, marca_de_tiempo: int=0) -> None:
        if  marca_de_tiempo == 0 or \
            marca_de_tiempo - self._cooldown_acciones['Velocidad'][0] > self._cooldown_acciones['Velocidad'][1]:
            saltos = abs(1 - self._velocidad_actual[0]) / 0.25
            if 1 - self._velocidad_actual[0] > 0.0:
                for _ in range(int(saltos)): press_and_release('Shift+.')
            else:
                for _ in range(int(saltos)): press('Shift') ; press(',') ; release('Shift')
            self._velocidad_actual[0] = 1.0
            self._cooldown_acciones['Velocidad'][0] = marca_de_tiempo
            print(f'Cambiando velocidad a {self._velocidad_actual[0]}')