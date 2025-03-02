
import os


from Scripts.pure_python import GaussianFilter as GaussianFilter_Python
from Scripts.only_numpy import GaussianFilter as GaussianFilter_Numpy
from Scripts.Cython.numpy_cython import GaussianFilter as GaussianFilter_Cython #type: ignore


os.system('clear')

filters = [
    GaussianFilter_Python(
        kernel_size = 15,
        sigma = 5.0
    ),
    GaussianFilter_Numpy(
        kernel_size = 15,
        sigma = 5.0
    ),
    GaussianFilter_Cython(
        kernel_size = 15,
        sigma = 5.0
    ),
]

for gaussian_filter in filters:
    images = gaussian_filter.load_images()
    filtered_images = gaussian_filter.apply_filter(images)
    gaussian_filter.save_images(filtered_images)
    print(f"Termino de aplicar filtros a: {gaussian_filter.__class__.__name__}")
