import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm 
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd 
plt.style.use("ggplot")


def get_func(opt="", options={}, id=None):
    if id == None:
        id = options[opt]
    if id == "id1":
        b = 10
        expression_function = lambda x, y: (x-1)**2 + b*(y-x**2)**2
    elif id == "id2":
        expression_function = lambda x, y: np.sin(x) + np.cos(y)
    elif id == "id3":
        expression_function = lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    return expression_function, id


def get_plot(option, options, min_max_x, min_max_y, STEP):
    func, id = get_func(option, options)
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
    
    return fig, id


def generate_dataframe(min_max_x, min_max_y, STEP):
    x = np.arange(min_max_x[0], min_max_x[1], STEP)
    y = np.arange(min_max_y[0], min_max_y[1], STEP)
    x, y = np.meshgrid(x, y)
    X_1, Y_1 = x.flatten(), y.flatten()
    df = pd.DataFrame({"X": X_1, "Y": Y_1})
    return df


def  get_parallel_coodi(df):
    df['index1'] = df.index
    # df = df.drop('individuals', axis=1)
    pivoted_df = df.pivot(index='index1', columns='gen', values='z')

    # Reset the index to make 'individuals' a regular column
    pivoted_df.reset_index(inplace=True)

    # Rename the columns if needed
    gen_names = [f'gen_{col}' for col in pivoted_df.columns[1:]]
    pivoted_df.columns = ['individuals'] + gen_names 
    print(pivoted_df)
    
    dimensions = []
    for i, col in enumerate(gen_names):
        dimension = dict(range = [np.min(pivoted_df[gen_names[-1]]), np.max(pivoted_df[gen_names[0]])],
                         label = col,
                         values = pivoted_df[f"{col}"])
        dimensions.append(dimension)
    fig = go.Figure(data=go.Parcoords(
        line = dict(color = pivoted_df[f'{gen_names[-1]}'],
                    colorscale = 'Portland_r',
                    showscale = True,
                    cmin = np.min(pivoted_df[f'{gen_names[-1]}']),
                    cmax = np.max(pivoted_df[f'{gen_names[-1]}'])),
             dimensions = list(dimensions)))
    fig.update_layout(margin={"b": 0, "l": 30, "r": 0 })
    # fig = px.parallel_coordinates(pivoted_df, color=gen_names[-1],
    #                               dimensions=gen_names,
    #                               color_continuous_scale=px.colors.diverging.Armyrose_r)
    return fig

def get_box_plot(df):
    fig = px.box(df, x="gen", y="z", points="all")
    return fig

def get_z_value(option, options, df):
    func, _ = get_func(option, options)
    df["z"] = df.apply(lambda row : func(row["individuals"][0], row["individuals"][1]), axis=1)
    return df