import threading
import os
import requests


def getter(url:str):
    response = await requests.get(url) #type: ignore
    print(response)
    return


if __name__ == '__main__':
    os.system('cls')
    urls = [
        "https://google.com"
        "https://raw.githubusercontent.com/pandas-dev/pandas/main/pandas/core/frame.py",
        "https://raw.githubusercontent.com/numpy/numpy/main/numpy/core/arrayprint.py",
        "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/linear_model/logistic.py",
        "https://raw.githubusercontent.com/tensorflow/tensorflow/main/tensorflow/python/keras/layers/core.py",
        "https://raw.githubusercontent.com/pytorch/pytorch/main/torch/nn/modules/activation.py",
        "https://raw.githubusercontent.com/pygame/pygame/main/pygame/sprite.py",
        "https://raw.githubusercontent.com/flask/flask/main/flask/views.py",
        "https://raw.githubusercontent.com/django/django/main/django/db/models/queryset.py"
    ]

    for url in urls:
        hilo = threading.Thread(target=getter,daemon=True)
        hilo.start()