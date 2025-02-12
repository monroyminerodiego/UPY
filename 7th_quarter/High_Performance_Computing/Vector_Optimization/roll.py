import numpy as np, time, os
from matplotlib import pyplot as plt
from difussion_problem import crear_gif, plot_grid

def laplacian(grid):
    return (
        np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + 
        np.roll(grid, 1, 1) + np.roll(grid, -1, 1) + 
        -4 * grid
    )

def evolve(grid, dt = 0.1, D = 1):
    return grid + dt * D * laplacian(grid)


def run_experiment(num_iterations):
    grid = np.zeros((600,600))
    grid[250:351,250:351] = 1.0
    

    for i in range(num_iterations):
        if i%(num_iterations//4) == 0:
            plot_grid(grid,True,i)

        grid = evolve(grid)
        

if __name__ == '__main__':
    os.system('clear')
    ex_time = time.time()
    run_experiment(6000)
    ex_time = time.time() - ex_time
    print(f"{'='*10} run_experiment: {ex_time:.05f} {'='*10}")

    crear_gif('./Imagenes/2D','./Imagenes/GIF/2D.gif')
    