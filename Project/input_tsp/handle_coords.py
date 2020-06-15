import requests
import os
import re

tsp_url = 'http://www.math.uwaterloo.ca/tsp/data/ml/mona-lisa100K.tsp'
filename = re.sub('tsp','txt', re.search(r'(?:.*)/(.*\.tsp)', tsp_url).group(1))
filepath = os.path.dirname(os.path.realpath('__file__'))
if os.path.split(filepath)[1]!='input_tsp':
    filepath = os.path.join(filepath, 'input_tsp')

def readCoords(batch=-7, meta_offset=6):
    coords = []
    with open(os.path.join(filepath, filename), "r") as file:
        for line in file.readlines()[meta_offset:batch+meta_offset]:
            node, x, y = line.split()
            coords.append({'node': node, 'x': int(x), 'y': int(y)})
    return coords

if __name__== '__main__':
    try:
        response = requests.get(tsp_url)
        with open(filename, "w") as file:
            file.write(response.text)
        fds=readCoords()
    except:
        print('!')