import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm 
import plotly.graph_objs as go
from scipy import optimize
plt.style.use("ggplot")


def get_func(opt:str, options:dict):
    id = options[opt]
    if id == "id1":
        b = 10
        expression_function = lambda x, y: (x-1)**2 + b*(y-x**2)**2
    elif id == "id2":
        expression_function = lambda x, y: np.sin(x) + np.cos(y)
    elif id == "id3":
        expression_function = lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    return expression_function


def get_plot(option, options, min_max_x, min_max_y, STEP):
    func = get_func(option, options)
    x = np.arange(min_max_x[0], min_max_x[1], STEP)
    y = np.arange(min_max_y[0], min_max_y[1], STEP)
    x, y = np.meshgrid(x, y)
    z = func(x, y)
    
    fig = {
        "data": 
            go.Surface(
                contours = {
                    "z": {"show": True, "usecolormap":True,
                          "highlightcolor":"limegreen", "project_z":True}
                    },
                z=z, 
                y=y, 
                x=x
                ),
        "layout": 
            go.Layout(
                height=700,
                scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
                margin=dict(l=65, r=50, b=65, t=90),
                uirevision='foo')
            }
    
    return fig
