import time 
import numpy as np 
import sys
import json 
import ast

def make_value(individual):
    b = 10 
    val = (individual[0]-1)**2 + b*(individual[1]-individual[0]**2)**2
    # time.sleep(1.0)
    # val = np.sin(individual[0]) + np.cos(individual[1])
    return val

if __name__ == "__main__":
    args = ast.literal_eval(sys.argv[1])
    val = make_value(args)
    with open('data.json', 'w') as f:
        json.dump({"val":val}, f)
    
    