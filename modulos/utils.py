import sys, os
from contextlib import contextmanager

RELACIONES = {
    'UNIDAD': {
        'uno':      '1',
        'un':       '1',
        'dos':      '2',
        'tres':     '3',
        'cuatro':   '4',
        'cinco':    '5',
        'seis':     '6',
        'siete':    '7',
        'ocho':     '8',
        'nueve':    '9'
    },
    'DECENA': {
        'treinta':      '3',
        'cuarenta':     '4',
        'cincuenta':    '5',
        'sesenta':      '6',
        'setenta':      '7',
        'ochenta':      '8',
        'noventa':      '9'
    },
    'DECENAS': {
        'diez':         '10',
        'once':         '11',
        'doce':         '12',
        'trece':        '13',
        'catorce':      '14',
        'quince':       '15',
        'dieciséis':    '16',
        'diecisiete':   '17',
        'dieciocho':    '18',
        'diecinueve':   '19',
        'veinte':       '20',
        'veintiuno':    '21',
        'veintidos':    '22',
        'veintitres':   '23',
        'veinticuatro': '24',
        'veinticinco':  '25',
        'veintiséis':   '26',
        'veintisiete':  '27',
        'veintiocho':   '28',
        'veintinueve':  '29',
        'treinta':      '30',
        'cuarenta':     '40',
        'cincuenta':    '50',
        'sesenta':      '60',
        'setenta':      '70',
        'ochenta':      '80',
        'noventa':      '90'
    },
    'CENTENA': {
        'ciento':           '1',
        'doscientos':       '2',
        'trescientos':      '3',
        'cuatrocientos':    '4',
        'quinientos':       '5',
        'seiscientos':      '6',
        'setecientos':      '7',
        'ochocientos':      '8',
        'novecientos':      '9'
    },
    'CENTENAS': {
        'cien':             '100',
        'doscientos':       '200',
        'trescientos':      '300',
        'cuatrocientos':    '400',
        'quinientos':       '500',
        'seiscientos':      '600',
        'setecientos':      '700',
        'ochocientos':      '800',
        'novecientos':      '900'
    }
}

STOPWORDS = ['y', 'segundos', 'segundo', 'minutos', 'minuto']

def transformar_numero(numero_recogido: str):
    cifras = [ cifra for cifra in numero_recogido.split(' ') if cifra not in STOPWORDS ]
    longitud_numero = len(cifras) 

    numero = ''

    try:
        if longitud_numero == 1:
            if cifras[0] in RELACIONES['UNIDAD'].keys():
                numero += RELACIONES['UNIDAD'][cifras[0]]
                return int(numero)
            
            if cifras[0] in RELACIONES['DECENAS'].keys():
                numero += RELACIONES['DECENAS'][cifras[0]]
                return int(numero)
            
            if cifras[0] in RELACIONES['CENTENAS'].keys():
                numero += RELACIONES['CENTENAS'][cifras[0]]
                return int(numero)

        if longitud_numero == 2:
            if cifras[0] in RELACIONES['DECENA'].keys():
                numero += RELACIONES['DECENA'][cifras[0]]
                numero += RELACIONES['UNIDAD'][cifras[1]]
                return int(numero)
            
            if cifras[0] in RELACIONES['CENTENA'].keys():
                numero += RELACIONES['CENTENA'][cifras[0]]

                if cifras[1] in RELACIONES['UNIDAD'].keys():
                    numero += '0'
                    numero += RELACIONES['UNIDAD'][cifras[1]]
                    return int(numero)
                
                if cifras[1] in RELACIONES['DECENAS'].keys():
                    numero += RELACIONES['DECENAS'][cifras[1]]
                    return int(numero)
        
        if longitud_numero == 3:
            numero += RELACIONES['CENTENA'][cifras[0]]
            numero += RELACIONES['DECENA'][cifras[1]]
            numero += RELACIONES['UNIDAD'][cifras[2]]
            return int(numero)
    except:
        pass
    
    return None


class ControlParada:

    def __init__(self) -> None:
        self.condicion_parada = False
    
    def finalizar_reproduccion(self) -> None:
        self.condicion_parada = True


@contextmanager
def silenciar_salida(to=os.devnull): # Si el log quiere guardarse aqui se pondría el nombre de un fichero
    fd = sys.stderr.fileno()

    def _redirigir_salida(to):
        sys.stderr.close() 
        os.dup2(to.fileno(), fd) 
        sys.stderr = os.fdopen(fd, 'w') 

    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open(to, 'w') as file:
            _redirigir_salida(to=file)
        try:
            yield 
        finally:
            _redirigir_salida(to=old_stdout)