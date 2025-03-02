import math
import os
import numpy as np
from PIL import Image

class GaussianFilter:
    def __init__(self, kernel_size: int = 3, sigma: float = 1.0):
        '''
        Clase que implementa un filtro Gaussiano para suavizar imágenes en escala de grises.
        
        ### Args:
        kernel_size (int): Tamaño del kernel (debe ser un número impar). Un valor mayor aumenta el desenfoque.
        sigma (float): Desviación estándar de la distribución Gaussiana. Un valor mayor incrementa la suavidad.
        '''
        self.kernel_size = kernel_size
        self.sigma = sigma
        self.location_path = os.path.dirname(os.path.dirname(__file__))
        self.kernel = self.generate_kernel()
    
    def generate_kernel(self):
        '''
        Genera un kernel Gaussiano de tamaño `kernel_size` y desviación estándar `sigma`.
        
        ### Returns:
        np.ndarray: Matriz 2D representando el kernel Gaussiano normalizado.
        '''
        offset = self.kernel_size // 2
        x, y = np.meshgrid(np.arange(-offset, offset + 1), np.arange(-offset, offset + 1))
        kernel = np.exp(-(x**2 + y**2) / (2 * self.sigma**2))
        kernel /= 2 * np.pi * self.sigma**2
        kernel /= kernel.sum()
        return kernel
    
    def apply_filter(self, images):
        '''
        Aplica el filtro Gaussiano a una lista de imágenes en escala de grises.
        
        ### Args:
        images (list): Lista de tuplas (nombre_archivo, matriz_imagen, width, height).
        
        ### Returns:
        list: Lista de tuplas (nombre_archivo, imagen_filtrada, width, height).
        '''
        filtered_images = []
        for filename, image, width, height in images:
            image_array = np.array(image, dtype=np.float32).reshape((height, width))
            padded_image = np.pad(image_array, self.kernel_size // 2, mode='constant', constant_values=0)
            new_image = np.zeros_like(image_array)
            
            for i in range(height):
                for j in range(width):
                    new_image[i, j] = np.sum(
                        padded_image[i:i+self.kernel_size, j:j+self.kernel_size] * self.kernel
                    )
            
            filtered_images.append((filename, new_image.astype(np.uint8), width, height))
        
        return filtered_images
    
    def load_images(self):
        '''
        Carga imágenes en escala de grises desde la carpeta `Files/Input`.
        
        ### Returns:
        list: Lista de tuplas (nombre_archivo, matriz_imagen, width, height) con las imágenes cargadas.
        '''
        input_path = os.path.join(self.location_path, 'Files', 'Input')
        images = []
        for filename in os.listdir(input_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                img_path = os.path.join(input_path, filename)
                img = Image.open(img_path).convert('L')  # Convertir a escala de grises
                width, height = img.size
                images.append((filename, np.array(img).flatten(), width, height))
        return images
    
    def save_images(self, images):
        '''
        Guarda una lista de imágenes filtradas en la carpeta `Files/Output`.
        
        ### Args:
        images (list): Lista de tuplas (nombre_archivo, imagen_filtrada, width, height).
        '''
        output_path = os.path.join(self.location_path, 'Files', 'Output','Only_numpy')
        os.makedirs(output_path, exist_ok=True)
        
        for filename, image, width, height in images:
            img = Image.fromarray(image.reshape((height, width)))
            img.save(os.path.join(output_path, f'blurred_{filename}'))
