import os

from cv2 import split

def create_dir():
    pastas = os.listdir('./results')
    if len(pastas) == 0:
        return 1
    else:
        indice = pastas[-1].split('_')
        indice = int(indice[1])+1
        return indice

create_dir()