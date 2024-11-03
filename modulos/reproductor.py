from abc import ABC, abstractclassmethod

class Reproductor:

    @abstractclassmethod
    def comenzar_reproduccion(self, terminar_reproduccion: callable) -> None: pass

    @abstractclassmethod
    def pausar_reproduccion(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def renaudar_reproduccion(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def alternar_pausa_reproduccion(self, marca_de_tiempo: int=0) -> None: pass
    
    @abstractclassmethod
    def saltar_hacia_delante(self, marca_de_tiempo: int=0, cantidad: int=5) -> None: pass

    @abstractclassmethod
    def saltar_hacia_atras(self, marca_de_tiempo: int=0, cantidad: int=5) -> None: pass
    
    @abstractclassmethod
    def reproducir_siguiente(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def reproducir_anterior(self, marca_de_tiempo: int=0) -> None: pass
    
    @abstractclassmethod
    def aumentar_velocidad(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def disminuir_velocidad(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def cambiar_velocidad(self, marca_de_tiempo: int=0) -> None: pass

    @abstractclassmethod
    def cerrar_reproductor(self) -> None: pass