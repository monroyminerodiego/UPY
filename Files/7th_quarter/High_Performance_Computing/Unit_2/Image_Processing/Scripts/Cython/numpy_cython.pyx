import math
import os
import numpy as np
from PIL import Image
from libc.math cimport exp, M_PI
cimport numpy as cnp

cdef class GaussianFilter:
    cdef int kernel_size
    cdef double sigma
    cdef cnp.ndarray kernel
    cdef str location_path
    
    def __init__(self, int kernel_size=3, double sigma=1.0):
        '''
        Clase que implementa un filtro Gaussiano para suavizar imágenes en escala de grises.
        
        ### Args:
        kernel_size (int): Tamaño del kernel (debe ser un número impar). Un valor mayor aumenta el desenfoque.
        sigma (float): Desviación estándar de la distribución Gaussiana. Un valor mayor incrementa la suavidad.
        '''
        self.kernel_size = kernel_size
        self.sigma = sigma
        self.location_path = os.path.dirname(os.path.dirname(__file__))
        self.location_path = os.path.dirname(self.location_path)
        self.kernel = self.generate_kernel()
    
    cdef cnp.ndarray generate_kernel(self):
        '''
        Genera un kernel Gaussiano de tamaño `kernel_size` y desviación estándar `sigma`.
        
        ### Returns:
        np.ndarray: Matriz 2D representando el kernel Gaussiano normalizado.
        '''
        cdef int offset = self.kernel_size // 2
        cdef cnp.ndarray[cnp.float64_t, ndim=2] kernel = np.zeros((self.kernel_size, self.kernel_size), dtype=np.float64)
        cdef int i, j
        cdef double x, y, value, sum_val = 0.0
        
        for i in range(self.kernel_size):
            for j in range(self.kernel_size):
                x, y = i - offset, j - offset
                value = (1 / (2 * M_PI * self.sigma ** 2)) * exp(-(x**2 + y**2) / (2 * self.sigma**2))
                kernel[i, j] = value
                sum_val += value
        
        kernel /= sum_val
        return kernel
    
    cpdef list apply_filter(self, list images):
        '''
        Aplica el filtro Gaussiano a una lista de imágenes en escala de grises.
        
        ### Args:
        images (list): Lista de tuplas (nombre_archivo, matriz_imagen, width, height).
        
        ### Returns:
        list: Lista de tuplas (nombre_archivo, imagen_filtrada, width, height).
        '''
        cdef list filtered_images = []
        cdef str filename
        cdef int width, height, i, j
        cdef cnp.ndarray[cnp.float32_t, ndim=2] image_array, padded_image, new_image
        cdef cnp.ndarray[cnp.uint8_t, ndim=2] result_image
        cdef int offset = self.kernel_size // 2
        
        for filename, image, width, height in images:
            image_array = np.array(image, dtype=np.float32).reshape((height, width))
            padded_image = np.pad(image_array, offset, mode='constant', constant_values=0)
            new_image = np.zeros((height, width), dtype=np.float32)
            
            for i in range(height):
                for j in range(width):
                    new_image[i, j] = np.sum(
                        padded_image[i:i+self.kernel_size, j:j+self.kernel_size] * self.kernel
                    )
            
            result_image = new_image.astype(np.uint8)
            filtered_images.append((filename, result_image, width, height))
        
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
        output_path = os.path.join(self.location_path, 'Files', 'Output','Cython_numpy')
        os.makedirs(output_path, exist_ok=True)
        
        for filename, image, width, height in images:
            img = Image.fromarray(image.reshape((height, width)))
            img.save(os.path.join(output_path, f'blurred_{filename}'))
