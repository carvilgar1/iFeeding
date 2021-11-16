import os
from whoosh import *
from whoosh import index
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser


PATH = './'
DIR = 'indice'
SCHEMA = Schema(
            id = ID(stored=True, unique=True),
            title = TEXT(stored = True),
            summary=TEXT(stored=True),
            ingredients=TEXT(stored=True),
            directions=TEXT(stored=True),
            nutrition=TEXT(stored=True),
        )


def crear_indice(ruta:str = PATH, nombre:str = DIR) -> None:
    if not os.path.exists(ruta + nombre):
        os.mkdir(ruta + nombre)
        indice = create_in(ruta+nombre, SCHEMA)
        indice.close()
    else:
        raise Exception('Este directorio ya existe')

def add_document(**kwargs):
    #index = open_dir(PATH+DIR)
    max = (None,-100000000000)
    for t in kwargs.items():
        print(t)
        if t[1] > max[1]:
            max = t
    return max

print(add_document(a=1, b=2,c=0, d=3))
