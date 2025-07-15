import os
import datetime
import inspect
import platform
from typing import Literal
from plyer import notification

class ExecutionError(BaseException):
    """
    Excepción generada por errores predefinidos en la ejecución de bots o utilidades.

    ### Atributos:
    * `error_string` (str): Descripción del error.
    """
    def __init__(self, error_string: str):
        super().__init__(error_string)

class DataError(BaseException):
    """
    Excepción generada por errores predefinidos en la ejecución de bots o utilidades.

    ### Atributos:
    * `error_string` (str): Descripción del error.
    """
    def __init__(self, error_string: str):
        super().__init__(error_string)

class Informer:
    # =============== CONSTRUCTOR METHODS ===============
    def __init__(self,verbose:bool=False,default_verbose_type:list[Literal['console','notification','.txt']] = ['console'],
                 log_file_path:str|None = None) -> None:
        '''
        Inicializa la clase Informer con capacidades de notificación.

        ### Atributos:
            * `verbose_type` (str): El modo predeterminado de notificación ('console' o 'notification').
            * `verbose` (bool): Determina si las notificaciones están activas o no.
            * `notifier` (ToastNotifier): La instancia del notificador para mostrar notificaciones.
        '''
        self.verbose       = verbose
        self.verbose_type  = default_verbose_type
        self.file_path     = log_file_path
        self.location_path = os.path.dirname(__file__)

    # =============== PRIVATE METHODS ===============
    def __validate_log_file(self) -> str:
        '''
        Valida y crea el archivo de log si no existe.

        ### Retorna:
            * `file_path` (str): Ruta del archivo de log validado.

        ### Excepciones:
            * `ExecutionError`: Si el archivo especificado en `self.file_path` no existe.
        '''
        if not(self.file_path):
            file_name = os.path.splitext(os.path.basename(inspect.stack()[-1].filename))[0]
            file_path = os.path.join(self.location_path,'Logs',f"{file_name}.txt")
            if not(os.path.isfile(file_path)):
                if not(os.path.exists(os.path.join(self.location_path,'Logs'))): os.mkdir(os.path.join(self.location_path,'Logs'))
                with open(file_path,'w'): self.file_path = file_path
            return file_path
        else:
            if not(os.path.exists(self.file_path)): raise ExecutionError(f"El archivo '{self.file_path}' no existe, favor de validarlo.")
            return self.file_path

    # =============== PUBLIC METHODS ===============
    def inform(self, message: str, mode: Literal['console','notification','.txt','default'] = 'default'):
        '''
        Informa al usuario con un mensaje.

        ### Args:
            * `message` (str): El mensaje que se transmitirá.
            * `mode` (str, opcional): El modo de notificación. Por defecto, se utiliza el atributo `verbose_type` de la clase.

        ### Notas:
            - Si `mode` es 'console', el mensaje se imprime en la consola.
            - Si `mode` es 'notification', se muestra una notificación con el título del archivo actual.
            - Si `mode` es '.txt', el mensaje se guarda en un archivo de log.
            - Si `verbose` es False, no se realiza ninguna acción.
        '''
        file_name = os.path.basename(inspect.stack()[-1].filename)

        if mode in ['console', 'notification','.txt']: validated_mode = mode
        else:                                          validated_mode = self.verbose_type


        if self.verbose and 'console' in validated_mode:
            print(message)
        
        if self.verbose and 'notification' in validated_mode:
            notification.notify(title = file_name, message = message,timeout = 1) # type: ignore
        
        if self.verbose and '.txt' in validated_mode:
            file = self.__validate_log_file()
            with open(file,'a') as file:
                localtime = str(datetime.datetime.now())[:19]
                file.write(f'{localtime}: {message.strip()}\n')

            
        

# ===== USAGE =====
if __name__ == '__main__':
    os.system('clear') if platform.system() == 'Linux' else os.system('cls')


    test = Informer(
        verbose              = True,
        default_verbose_type = ['console','notification','.txt'],
    )

    test.inform('Este es un msj de prueba enviado desde common')