import time 
import numpy as np 
import sys
import json 
import ast

def make_value(individual):
    b = 10 
    x = individual[0]
    y = individual[0]
    # val = (individual[0]-1)**2 + b*(individual[1]-individual[0]**2)**2
    # time.sleep(1.0)
    # val = np.sin(individual[0]) + np.cos(individual[1])
    val = (x**2 + y - 11)**2 + (x + y**2 - 7)**2 
    return val

if __name__ == "__main__":
    args = ast.literal_eval(sys.argv[1])
    val = make_value(args)
    with open('code/data.json', 'w') as f:
        json.dump({"val":val}, f)
    
