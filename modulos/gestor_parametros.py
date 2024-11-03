import sys
import json
from argparse import ArgumentParser

MODOS_REPRODUCCION = {
    'nativo': 'local',
    'youtube': 'yt'
}

class GestorParametros:

    def __init__(self) -> None:
        self._parseador = ArgumentParser(
            description='Asistente multimodal para la reproducción de videos locales o desde Youtube. Para utilizarlo en youtube se debe dejar el programa ejecutando en segundo plano en modo "yt" y enfocar la ventana del navegador.'
        )

        self._parseador.add_argument(
            'modo_reproduccion',
            choices=MODOS_REPRODUCCION.values(),
            help='Modo de ejecución del programa. Se debe elegir entre reproducción reproducción local o en Youtube.'
        )
        self._parseador.add_argument(
            '-v', '--lista-videos',
            nargs='*',
            help='Ruta de los videos que se quieren reproducir en local.'
        )
        self._parseador.add_argument(
            '--no-identificar-habla',
            action='store_true',
            help='Flag para no iniciar la identificación por habla.'
        )
        self._parseador.add_argument(
            '--no-identificar-gestos',
            action='store_true',
            help='Flag para no iniciar la identificación por gestos.'
        )
        self._parseador.add_argument(
            '-c', '--comandos-voz',
            nargs=1,
            help='Fichero JSON con los comandos de voz personalizados siguiendo la estructura del ejemplo'
        )

    
    def extraer_parametros(self, argumentos):
        parametros = self._parseador.parse_args(argumentos)

        if parametros.comandos_voz:
            try:
                with open(parametros.comandos_voz, mode='r', encoding='utf-8') as lista_instrucciones_voz:
                    json.load(lista_instrucciones_voz)
            except:
                print('El fichero con los comandos de voz no es válido.')
                sys.exit(4)

        if parametros.modo_reproduccion == 'local' and not parametros.lista_videos:
            print('Al reproducir en local se necesitan pasar por argumento los archivos de video:')
            self._parseador.print_usage()
            sys.exit(2)
        
        return parametros