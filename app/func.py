import time 
import numpy as np 
import sys
import json 
import ast
from utils_app import get_func


def make_value(individual, id):
    x = individual[0]
    y = individual[1]
    func, _ = get_func(id=id)
    val = func(x, y)
    return val

if __name__ == "__main__":
    individual = ast.literal_eval(sys.argv[2])
    id = str(sys.argv[1])
    
    val = make_value(individual, id)
    with open('saves/data.json', 'w') as f:
        json.dump({"val":val}, f)
    
