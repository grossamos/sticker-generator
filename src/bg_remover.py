from rembg import remove
from .util import STATIC_PATH

def remove_background(input_path: str, output_path: str):
    with open(STATIC_PATH + input_path, 'rb') as i:
        with open(STATIC_PATH + output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

