import os
from typing import Literal
import platform
import pyautogui as py
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

from common import Informer

class Spyder:
	# =============== CONSTRUCTOR ===============
	def __init__(self,images_folder:str|None=None,web_driver:webdriver.Chrome|None=None,web_driver_options:Options|None=None,
			  verbose:bool=False,verbose_type:list[Literal['console','notification','.txt']] = ['console'], debugging:bool = False,
			  log_file_path:str|None = None):
		'''
        Clase que proporciona funcionalidades de automatización utilizando Selenium y PyAutoGUI.

        ### Args:
        * `images_folder` (str, opcional): La carpeta donde se almacenan las imágenes para las operaciones de búsqueda. Por defecto es None.
        * `web_driver` (webdriver.Chrome, opcional): Una instancia del controlador web de Chrome. Por defecto es None.
        * `web_driver_options` (Options, opcional): Las opciones del controlador web de Chrome. Por defecto es None.
        * `verbose` (bool, opcional): Si se deben habilitar mensajes informativos. Por defecto es False.
        * `verbose_type` (Literal['console', 'notification'], opcional): El tipo de mensajes informativos, ya sea 'console' o 'notification'. Por defecto es 'console'.
        * `debugging` (bool, opcional): Si se deben habilitar opciones de depuración. Por defecto es False.

        ### Atributos:
        * `driver_options` (Options): Las opciones del controlador web.
        * `driver` (webdriver.Chrome): La instancia del controlador web de Chrome.
        * `images_folder` (str): La carpeta donde se almacenan las imágenes.
        * `verbose` (bool): Si se deben habilitar mensajes informativos.
        * `verbose_type` (str): El tipo de mensajes informativos.
        * `debugging` (bool): Si se deben habilitar opciones de depuración.
        * `info` (Informer): Una instancia de Informer para manejar mensajes informativos.
        '''
		# Staring the variables
		self.driver_options = web_driver_options
		self.driver         = web_driver
		self.images_folder  = images_folder
		self.verbose        = verbose
		self.verbose_type   = verbose_type
		self.debugging      = debugging
		self.system         = platform.system()

		self.info = Informer(
			verbose = verbose,
			default_verbose_type = verbose_type,
			log_file_path = log_file_path
		)

	# =============== PUBLIC METHODS ===============
	def start_session_selenium(self,experimental_options:bool = True,maximized:bool = True,ignore_certificate_errors:bool = True,
							return_actions:bool = False,headless:bool = False):
		"""
		Inicia una sesión de Selenium con el controlador de Chrome configurado.

		### Args:
		- `experimental_options` (bool, opcional): Si es True, configura opciones experimentales para el controlador de Chrome. Por defecto es True.
		- `maximized` (bool, opcional): Si es True, inicia la ventana del navegador maximizada. Por defecto es True.
		- `ignore_certificate_errors` (bool, opcional): Si es True, ignora los errores de certificado. Por defecto es True.
		- `return_actions` (bool, opcional): Si es True, devuelve una instancia de ActionChains junto con el controlador. Por defecto es False.

		### Retorna:
		- `driver` (webdriver.Chrome): Una instancia del controlador de Chrome configurada.
		- `actions` (ActionChains, opcional): Una instancia de ActionChains asociada con el controlador de Chrome, si `return_actions` es True.
		"""
		service = Service(ChromeDriverManager().install())
		options = Options()
		options.add_experimental_option("prefs", {
			"credentials_enable_service": False,
			"profile.password_manager_enabled": False
		})
		if maximized:                 options.add_argument("--start-maximized")
		if ignore_certificate_errors: options.add_argument('--ignore-certificate-errors')
		if headless:
			options.add_argument("--headless")
			options.add_argument("--disable-gpu")
		if experimental_options:
			options.add_experimental_option("excludeSwitches", ["enable-automation"])
			options.add_experimental_option('useAutomationExtension', False)
			options.add_argument("--disable-blink-features=AutomationControlled")
		driver  = webdriver.Chrome(options=options, service=service)
		actions = ActionChains(driver)

		return (driver, actions) if return_actions else driver

	def enable_mayusc(self,state:bool=True):
		'''
        Activa o desactiva la tecla 'Caps Lock'.

        ### Args:
        * `state` (bool, opcional): El estado deseado para la tecla 'Caps Lock'. Por defecto es True (activado).        
        '''
		current_state = self.__validate_caps_lock()
		if current_state != state:
			py.press('capslock')
			self.info.inform(f"\tCapslock pressed...")

	def locate_image_on_screen(self,image_name:str,invert:bool=False,timeout:int=90,confidence:float=0.9,region:tuple|None=None): 
		'''
        Ubica una imagen en la pantalla.

        ### Args:
        * `image_name` (str): El nombre de la imagen a buscar.
        * `invert` (bool, opcional): Si se debe invertir la búsqueda. Por defecto es False.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.
        * `confidence` (float, opcional): El nivel de confianza para la coincidencia de la imagen. Por defecto es 0.9.
        * `region` (tuple, opcional): La región de la pantalla para realizar la búsqueda. Por defecto es None.

        ### Retorna:
        * La ubicación de la imagen si se encuentra, de lo contrario None.
        '''
		for _ in range(timeout):
			try:
				located = py.locateOnScreen(os.path.join(self.images_folder,image_name),confidence=confidence, region=region) #type:ignore
			except:
				located = None
			if (located and not(invert)) or (not(located) and invert):
				self.info.inform(f"\t'{image_name}' {'no longer located' if invert else 'located'}...")
				return located
			py.sleep(1)
		self.info.inform(f"\t'{image_name}' {'is still located' if invert else 'is not located'}...")
		return None
	
	def locate_images_on_screen(self,images_list_names:list,timeout:int=90,confidence:float=0.9,region:tuple|None=None,Return:Literal['location','image_name']='location'):
		'''
        Ubica una de las múltiples imágenes en la pantalla.

        ### Args:
        * `images_list_names` (list): Lista de nombres de imágenes a buscar.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.
        * `confidence` (float, opcional): El nivel de confianza para la coincidencia de la imagen. Por defecto es 0.9.
        * `region` (tuple, opcional): La región de la pantalla para realizar la búsqueda. Por defecto es None.
        * `Return` (Literal['location', 'image_name'], opcional): Qué devolver, ya sea la ubicación de la imagen o el nombre de la imagen encontrada. Por defecto es 'location'.

        ### Retorna:
        * La ubicación de la imagen o el nombre de la imagen encontrada si se encuentra, de lo contrario None.
        '''
		for _ in range(timeout):
			for image_name in images_list_names:
				try:
					location = py.locateOnScreen(os.path.join(self.images_folder,image_name),confidence=confidence, region=region) #type:ignore
				except:
					location = None
				if location != None:
					self.info.inform(f"\t'{image_name}' located...")
					return location if Return == 'location' else image_name
			py.sleep(1)
		self.info.inform(f"\tNeither of the images were located...")
		return None
	
	def click_image_on_screen(self,image_name:str,timeout:int=90,confidence:float=0.9,region:tuple|None=None):
		'''
        Hace clic en una imagen en la pantalla.

        ### Args:
        * `image_name` (str): El nombre de la imagen a hacer clic.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.
        * `confidence` (float, opcional): El nivel de confianza para la coincidencia de la imagen. Por defecto es 0.9.
        * `region` (tuple, opcional): La región de la pantalla para realizar la búsqueda. Por defecto es None.

        ### Retorna:
        * La ubicación de la imagen si se hace clic con éxito, de lo contrario None.
        '''
		for _ in range(timeout):
			try:
				located = py.locateOnScreen(os.path.join(self.images_folder,image_name),confidence=confidence, region=region) #type:ignore
			except:
				located = None
			if located:
				py.click(located)
				self.info.inform(f"\t'{image_name}' clicked...")
				return located
			py.sleep(1)
		self.info.inform(f"\t'{image_name}' not clicked...")
		return None
			
	def validate_end_loading(self,consecutive_contdowns_limit:int=5,timeout:int=90,region:tuple|None=None,
							validation_type:Literal['pyautogui','selenium'] = 'pyautogui',object:webdriver.Chrome = None):
		'''
        Valida si la pantalla ha dejado de cambiar.

        ### Args:
        * `consecutive_contdowns_limit` (int, opcional): El número de capturas consecutivas iguales para considerar que la pantalla ha dejado de cambiar. Por defecto es 5.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.
        * `region` (tuple, opcional): La región de la pantalla para realizar la validación. Por defecto es None.

        ### Retorna:
        * `True` si la pantalla ha dejado de cambiar, de lo contrario None.
        '''
		if validation_type == 'pyautogui':
			self.__validate_no_temp_images()
			consecutive_contdowns = 0
			image1 = py.screenshot('.temporary_image1.png', region=region); image1 = np.array(image1)
			for _ in range(timeout):
				py.sleep(0.45)
				image2 = py.screenshot('.temporary_image2.png', region=region); image2 = np.array(image2)
				py.sleep(0.45)
				difference = np.sum(image1 != image2)
				if difference == 0: consecutive_contdowns += 1
				else: consecutive_contdowns = 0
				if consecutive_contdowns >= consecutive_contdowns_limit:
					self.info.inform(f"\tPyAutoGUI screen's not changing anymore...")
					os.remove('.temporary_image2.png'); os.remove('.temporary_image1.png')
					return True
				py.sleep(0.45)
				image1 = py.screenshot('.temporary_image1.png', region=region); image1 = np.array(image1)
				py.sleep(0.45)
			self.info.inform(f"\t({timeout}) Timeout reached and PyAutoGUI screen is still moving...")
			os.remove('.temporary_image2.png'); os.remove('.temporary_image1.png')
			return None
		elif validation_type == 'selenium':
			completed_loading = WebDriverWait(object,timeout).until(
				lambda driver: driver.execute_script('return document.readyState') == 'complete'
			)
			if completed_loading: self.info.inform("\tSelenium screens not changing anymore...")
			else: self.info.inform(f"\t({timeout}) Timeout reached and selenium screen is still moving...")
			return completed_loading

	def click_element_on_screen(self,object:webdriver.Chrome,by:Literal['id','xpath','link text','partial link text','name','tag name','class name','css selector'],element:str,timeout:int=90):
		'''
        Hace clic en un elemento en la pantalla utilizando Selenium.

        ### Args:
        * `object` (str): El objeto que contiene el elemento.
        * `by` (str): El método para localizar el elemento.
        * `element` (str): El elemento a hacer clic.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.

        ### Retorna:
        * El elemento si se hace clic con éxito, de lo contrario None.
        '''
		try:
			tag = self.validate_element_on_screen(object,by,element,timeout)
			tag.click()
			self.info.inform(f"\t{by.upper()}: {element[-20:]} clicked...")
			return tag
		except Exception as ex:
			self.info.inform(f"\t{by.upper()}: {element[-20:]} not clicked because '{ex}'...")
			return None
	
	def validate_element_on_screen(self,object:webdriver.Chrome,by:Literal['id','xpath','link text','partial link text','name','tag name','class name','css selector'],element:str,timeout:int=90):
		'''
        Valida la presencia de un elemento en la pantalla utilizando Selenium.

        ### Args:
        * `object` (str): El objeto que contiene el elemento.
        * `by` (str): El método para localizar el elemento (por ejemplo, 'id', 'name', 'xpath').
        * `element` (str): El elemento a validar.
        * `timeout` (int, opcional): El tiempo máximo de espera en segundos. Por defecto es 90.

        ### Retorna:
        * El elemento si se valida con éxito, de lo contrario None.
        '''
		try:
			tag = WebDriverWait(object, timeout).until(EC.presence_of_element_located((by,element)))
			self.info.inform(f"\t{by.upper()}: {element[-20:]} located...")
			return tag
		except:
			self.info.inform(f"\t{by.upper()}: {element[-20:]} not located...")
			return None
	
	# =============== PRIVATE METHODS ===============
	def __validate_no_temp_images(self):
		'''
        Valida y elimina imágenes temporales si existen.
        '''
		if (os.path.exists('.temporary_image1.png')) or (os.path.exists('.temporary_image2.png')): self.info.inform('Deleted remaining images...')
		if os.path.exists('.temporary_image1.png'): os.remove('.temporary_image1.png')
		if os.path.exists('.temporary_image2.png'): os.remove('.temporary_image2.png')

	def __validate_caps_lock(self):
		'''
		Verifica el estado actual de la tecla 'Caps Lock'.

		### Returns:
		* `True` si la tecla 'Caps Lock' está activada.
		* `False` si la tecla 'Caps Lock' está desactivada.
		'''
		current_os = platform.system()
		
		if current_os == "Windows":
			return self.__validate_caps_lock_windows()
		elif current_os == "Linux":
			return self.__validate_caps_lock_linux()
		else:
			raise NotImplementedError("Unsupported operating system")

	def __validate_caps_lock_windows(self):
		import win32api
		import win32con
		return bool(win32api.GetKeyState(win32con.VK_CAPITAL) & 0x0001)

	def __validate_caps_lock_linux(self):
		import evdev
		caps_lock = False
		devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
		for device in devices:
			caps_lock_state = evdev.ecodes.KEY_CAPSLOCK
			if caps_lock_state in device.capabilities().get(evdev.ecodes.EV_KEY, []):
				for event in device.read():
					if event.type == evdev.ecodes.EV_KEY and event.code == caps_lock_state:
						caps_lock = bool(event.value)
						break
		return caps_lock


# =============== USAGE ===============
if __name__ == '__main__':
	os.system('cls') if platform.system() == 'Windows' else os.system('clear')

	test = Spyder(
		web_driver         = None,
		web_driver_options = None,
		images_folder      = 'Files/Images/AsignacionEquipos/Debugging',
		verbose            = True,
		debugging          = True,
	)

	test.enable_mayusc(False)