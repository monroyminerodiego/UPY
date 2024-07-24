import time, os
from common import Informer, ExecutionError
from simulator import Spyder

info = Informer(True)

def main(username:str,psswrd:str):
    os.system('xhost +')
    os.system('clear')
    spyder = Spyder(verbose = True)

    driver, driver_actions = spyder.start_session_selenium(return_actions=True)

    driver.get('https://demoqa.com/login')

    element_path = '//*[@id="userName"]'
    element = spyder.click_element_on_screen(driver,'xpath',element_path)
    if not(element): raise ExecutionError("No se encontró el botón de 'UserName'")
    time.sleep(0.5)

    element.send_keys(username); time.sleep(0.5)

    element_path = '//*[@id="password"]'
    element = spyder.click_element_on_screen(driver,'xpath',element_path)
    if not(element): raise ExecutionError("No se encontró el botón de 'UserName'")
    time.sleep(0.5)

    element.send_keys(psswrd); time.sleep(0.5)

    # TODO: Crear scroll para que se vea visible el login

    element_path = '//*[@id="login"]'
    element = spyder.click_element_on_screen(driver,'xpath',element_path)
    if not(element): raise ExecutionError("No se encontró el botón de 'Login'")
    time.sleep(0.5)

    spyder.validate_end_loading(validation_type='selenium',object=driver)

    element_path = '//*[@id="name"]'
    element = spyder.validate_element_on_screen(driver,'xpath',element_path,3)
    if element: raise ExecutionError("Credenciales incorrectas")
    time.sleep(0.5)

    info.inform("Inicio de Sesion Correcto")

try:
    execution_time = time.time()
    main(
        username='diego',
        psswrd='ashjash#',
    )
except ExecutionError as ex: info.inform(str(ex))
except Exception as ex:
    info.inform(str(ex))
    raise ex
finally:
    execution_time = time.time() - execution_time
    info.inform(f"{'*'*15} Tiempo ejecucion: {execution_time:.02f} segundos {'*'*15}")