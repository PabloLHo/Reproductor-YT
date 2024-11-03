import sys
import os
sys.path.append(os.path.abspath('.\\modulos'))

from modulos.gestor_parametros import GestorParametros, MODOS_REPRODUCCION
from modulos.utils import ControlParada
from modulos.identificador_habla import IdentificadorHabla
from modulos.identificador_gestos import IdentificadorGestos
from modulos.reproductor_yt import ReproductorYT
from modulos.reproductor_nativo import ReproductorNativo


## Extracción de parámetros ##

parametros = GestorParametros().extraer_parametros(sys.argv[1:])

## Inicialización ##

if parametros.modo_reproduccion == MODOS_REPRODUCCION['nativo']:
    lista_videos = [ os.path.abspath(video) for video in parametros.lista_videos ]
    reproductor = ReproductorNativo(lista_videos)
elif parametros.modo_reproduccion == MODOS_REPRODUCCION['youtube']:
    reproductor = ReproductorYT()
else:
    print('No se reconoce el modo de reproducción.')
    sys.exit(3)

identificador_gestos = IdentificadorGestos(reproductor)
identificador_habla = IdentificadorHabla(reproductor)

control_parada = ControlParada()

def finalizar_reproduccion():
    control_parada.finalizar_reproduccion()
    try:
        identificador_gestos.finalizar_identificacion()
        identificador_habla.finalizar_identificacion()
        reproductor.cerrar_reproductor()
    except RuntimeError:
        sys.exit(1) # Aborta ejecución


## Puesta en marcha ##

reproductor.comenzar_reproduccion(finalizar_reproduccion)

if not parametros.no_identificar_habla:
    identificador_habla.comenzar_identificacion(finalizar_reproduccion)

if not parametros.no_identificar_gestos:
    identificador_gestos.comenzar_identificacion(finalizar_reproduccion) # Bloqueante
else:
    # Bloquear hasta finalizar
    while not control_parada.condicion_parada: pass