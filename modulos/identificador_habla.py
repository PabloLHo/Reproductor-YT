import os
from speech_recognition import Recognizer, Microphone, AudioData
from speech_recognition import UnknownValueError, RequestError
from reproductor import Reproductor
from utils import transformar_numero
from Levenshtein import ratio
import json


def override_recognize_vosk(self, audio_data, language='en', path='model'):
    from vosk import KaldiRecognizer, Model, SetLogLevel

    assert isinstance(audio_data, AudioData), "Data must be audio data"
    
    if not hasattr(self, 'vosk_model'):
        SetLogLevel(-3)
        if not os.path.exists(path):
            return "Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder."
            exit (1)
        self.vosk_model = Model(path)

    rec = KaldiRecognizer(self.vosk_model, 16000);
        
    rec.AcceptWaveform(audio_data.get_raw_data(convert_rate=16000, convert_width=2));
    finalRecognition = rec.FinalResult()
        
    return finalRecognition

Recognizer.recognize_vosk = override_recognize_vosk


class IdentificadorHabla:

    def __init__(self, reproductor: Reproductor, comandos_voz: str='./comandos_voz.json') -> None:
        self._identificador_audio = Recognizer()
        self._microfono = Microphone()
        self._reproductor = reproductor

        self._callback_finalizacion = None
        self._terminar_identificacion = None

        # Calibrar la entrada de audio
        with self._microfono as entrada_audio:
            self._identificador_audio.adjust_for_ambient_noise(entrada_audio)

        # Carga de los comandos de voz
        with open(comandos_voz, mode='r', encoding='utf-8') as lista_instrucciones_voz:
            self._comandos_voz: dict = json.load(lista_instrucciones_voz)
    
    def _identificar_comando(self, entrada: str) -> any:
        if not entrada: return None, None

        mejor_coincidencia = ''
        menor_distancia = 0.0
        for accion in self._comandos_voz.keys():
            
            comando_recibido = entrada.split()[0] \
            if accion == 'Saltar tiempo adelante' or accion == 'Saltar tiempo atrás' \
            else entrada

            for comando in self._comandos_voz[accion]:
                distancia = ratio(comando_recibido, comando, score_cutoff=0.8)
                if  distancia > menor_distancia:
                    menor_distancia = distancia
                    mejor_coincidencia = accion

        if menor_distancia > 0.8: 
            if  mejor_coincidencia == 'Saltar tiempo adelante' or accion == 'Saltar tiempo atrás' and \
                len(entrada.split()) > 1:
                return mejor_coincidencia, transformar_numero(' '.join(entrada.split()[1:]))
            return mejor_coincidencia, None
        return None, None
    
    def _identificar_audio(self, identificador_audio: Recognizer, audio: AudioData) -> None:
        try:
            comando = json.loads(identificador_audio.recognize_vosk(audio, path='modelo_identificacion_habla'))['text']
            accion, valor = self._identificar_comando(comando)
            if accion == "Cierra video":
                self._callback_finalizacion()
            elif accion == 'Pausar video':
                self._reproductor.pausar_reproduccion()
            elif accion == 'Renaudar video':
                self._reproductor.renaudar_reproduccion()
            elif accion == 'Siguiente video':
                self._reproductor.reproducir_siguiente()
            elif accion == 'Anterior video':
                self._reproductor.reproducir_anterior()
            elif accion == 'Disminuir velocidad':
                self._reproductor.disminuir_velocidad()
            elif accion == 'Aumentar velocidad':
                self._reproductor.aumentar_velocidad()
            elif accion == 'Saltar tiempo atrás':
                self._reproductor.saltar_hacia_atras() \
                if valor is None else self._reproductor.saltar_hacia_atras(cantidad=valor)
            elif accion == 'Saltar tiempo adelante':
                self._reproductor.saltar_hacia_delante() \
                if valor is None else self._reproductor.saltar_hacia_delante(cantidad=valor)
            else:
                # print('No entiendo el comando de voz')
                pass
        except UnknownValueError:
            # print('No entiendo el comando de voz')
            pass
        except RequestError as request_error:
            print(f'Identificador de audio no disponible: {request_error}')
    

    def comenzar_identificacion(self, callback_finalizacion: callable) -> None:
        if self._terminar_identificacion is None:
            self._callback_finalizacion = callback_finalizacion
            self._terminar_identificacion = self._identificador_audio.listen_in_background(self._microfono, self._identificar_audio)


    def finalizar_identificacion(self) -> None:
        if self._terminar_identificacion is not None:
            self._terminar_identificacion(wait_for_stop=True)
            self._terminar_identificacion = None