import math
import os
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
        list: Matriz 2D representando el kernel Gaussiano normalizado.
        '''
        kernel = []
        sum_val = 0
        offset = self.kernel_size // 2
        
        for i in range(self.kernel_size):
            row = []
            for j in range(self.kernel_size):
                x, y = i - offset, j - offset
                value = (1 / (2 * math.pi * self.sigma ** 2)) * math.exp(-(x**2 + y**2) / (2 * self.sigma**2))
                row.append(value)
                sum_val += value
            kernel.append(row)
        
        # Normalizar el kernel
        for i in range(self.kernel_size):
            for j in range(self.kernel_size):
                kernel[i][j] /= sum_val
        
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
            image_2d = [image[i * width:(i + 1) * width] for i in range(height)]
            height, width = len(image_2d), len(image_2d[0])
            offset = self.kernel_size // 2
            new_image = [[0] * width for _ in range(height)]
            
            for i in range(offset, height - offset):
                for j in range(offset, width - offset):
                    value = 0
                    for ki in range(self.kernel_size):
                        for kj in range(self.kernel_size):
                            ni, nj = i + ki - offset, j + kj - offset
                            value += image_2d[ni][nj] * self.kernel[ki][kj]
                    new_image[i][j] = int(value)
            
            filtered_images.append((filename, new_image, width, height))
        
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
                images.append((filename, list(img.getdata()), width, height))
        return images
    
    def save_images(self, images):
        '''
        Guarda una lista de imágenes filtradas en la carpeta `Files/Output`.
        
        ### Args:
        images (list): Lista de tuplas (nombre_archivo, imagen_filtrada, width, height).
        '''
        output_path = os.path.join(self.location_path, 'Files', 'Output','Pure_python')
        os.makedirs(output_path, exist_ok=True)
        
        for filename, image, width, height in images:
            img = Image.new('L', (width, height))
            img.putdata([pixel for row in image for pixel in row])
            img.save(os.path.join(output_path, f'blurred_{filename}'))
