import numpy as np
import pandas as pd
from genetic_alg import genetic_algorithm
import logging
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib import cm
plt.style.use("ggplot")


def make_function(x, y):
    b = 10 
    return (x-1)**2 + b*(y-x**2)**2


def plotting(X, Y, Z, x, y, z, best):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=.6,
                           linewidth=0, antialiased=False)
    ax.scatter(x, y, z, c='red', marker='.', s=100)
    
    for i in range(len(best[0])):
        current_z = make_function(best[0][i], best[1][i])
        ax.scatter(best[0][i], best[1][i], current_z, c='blue', marker='.', s=100)
        if i > 0:  # Draw line segment from previous point to current point
            prev_z = make_function(best[0][i-1], best[1][i-1])
            ax.plot([best[0][i-1], best[0][i]], [best[1][i-1], best[1][i]], 
                    [prev_z, current_z], color='green', linestyle='-', linewidth=2)
    # Customize the z axis.
    ax.set_zlim(0, 200)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def main():
    logging.basicConfig(filename="test.log", format='%(asctime)s %(message)s', filemode='w') 
    logger = logging.getLogger() 
    logger.setLevel(logging.DEBUG)
    
    x = np.arange(-2, 2, 0.15)
    y = np.arange(-1, 3, 0.15)
    X, Y = np.meshgrid(x, y)
    Z = make_function(X, Y)
    
    X_1, Y_1 = X.flatten(), Y.flatten()
    df = pd.DataFrame({"X": X_1, "Y": Y_1})
    
    best_individuals = genetic_algorithm(df, logger=logger)
    print(best_individuals)
    best_individuals = np.asarray(best_individuals).T
    plotting(X, Y, Z, x=0, y=0, z=0, best=best_individuals)
    
