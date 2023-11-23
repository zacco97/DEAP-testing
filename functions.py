import numpy as np
import pandas as pd
from genetic_alg import genetic_algorithm
import logging
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib import cm
plt.style.use("ggplot")


def make_function(x, y):
    return np.sin(x) + np.cos(y)


def plotting(X, Y, Z, x, y, z, best):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=.6,
                           linewidth=0, antialiased=False)
    ax.scatter(x, y, z, c='red', marker='.', s=100)
    ax.scatter(best[0], best[1], make_function(best[0], best[1]), c='blue', marker='.', s = 100)
    # Customize the z axis.
    ax.set_zlim(-2.01, 2.01)
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
    
    x = np.linspace(0, 6, 100)
    y = np.linspace(0, 6, 100)
    X, Y = np.meshgrid(x, y)
    Z = make_function(X, Y)
    
    X_1, Y_1 = X.flatten(), Y.flatten()
    df = pd.DataFrame({"X": X_1, "Y": Y_1})
    
    best_individuals = genetic_algorithm(df, logger=logger)
    print(best_individuals)
    best_individuals = np.asarray(best_individuals).T
    plotting(X, Y, Z, x=4.7, y=3, z=np.sin(4.7) + np.cos(3), best=best_individuals)
    
