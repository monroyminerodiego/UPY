'''
Para ejecutarel código: py -m kernprof -l -v difussion_problem.py
'''

import matplotlib.pyplot as plt
import os
from PIL import Image

def plot_u(u, time):
    plt.plot(u)
    plt.xlabel("Position")
    plt.ylabel(f"t = {time}")
    plt.ylim(0,1.2)
    plt.savefig(f'Imagenes/1D/imagen_{str(time).replace('.','_').replace(',','_')}.png')
    plt.close()

# ===== Creacion de GIF
def crear_gif(imagenes_path:str,output_name:str):
    imagenes = sorted(os.listdir(imagenes_path))
    frames = [Image.open(os.path.join(imagenes_path,imagen)) for imagen in imagenes]
    frames[0].save(
        output_name,
        save_all=True,
        append_images=frames[1:],
        duration=500,  # Duración de cada frame en milisegundos
        loop=0  # 0 significa que el GIF se repetirá infinitamente
    )
    print("GIF guardado")

# @profile #type: ignore
def evolve(grid, grid_out, dt = 0.1, D = 1.0):
    xmax, ymax = grid_shape # Particular situation considering dx = 1 and dy = 1
    
    for i in range(xmax):
        for j in range(ymax):
            dxx = grid[(i+1)%xmax][j] + grid[(i-1)%xmax][j] - 2 * grid[i][j] # / (dx)**2
            dyy = grid[i][(j+1)%ymax] + grid[i][(j-1)%ymax] - 2 * grid[i][j] # / (dy)**2
            grid_out[i][j] = grid[i][j]+D * (dxx + dyy) * dt

def plot_grid(grid,save:bool = False,consecutive:int = 0):
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    
    if not(save): plt.show()
    else:
        plt.savefig(f'Imagenes/2D/{consecutive}.png')
        plt.close()
    
def run_experiment(num_iterations):
    xmax, ymax = grid_shape
    new_grid = [[0.0]*ymax for x in range(xmax)]
    next_grid = [[0.0]*ymax for x in range(xmax)]
    
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            if (i >= 250) and (i <= 350) and (j >= 250) and (j<=350):
                new_grid[i][j] = 1.0

    for i in range(num_iterations):
        if i%(num_iterations//4) == 0:
            plot_grid(new_grid,True,i)
        evolve(new_grid,next_grid)
        new_grid, next_grid = next_grid, new_grid


if __name__ == '__main__':
    # ====== Creacion de carpetas
    location_path = os.path.dirname(__file__)
    d1 = os.path.join(location_path,'Imagenes','1D')
    d2 = os.path.join(location_path,'Imagenes','2D')
    gif = os.path.join(location_path,'Imagenes','GIF')
    os.makedirs(d1,exist_ok=True)
    os.makedirs(d2,exist_ok=True)
    os.makedirs(gif,exist_ok=True)

    # ====== Parameter definition
    xmax = 500
    dx = 1
    grid_shape = xmax // dx

    u = [0.0] * grid_shape
    D = 1
    tmax = 10_000
    dt = 0.1

    # ===== Set Initial Conditions
    for i in range(grid_shape):
        if i >= 200 and i <= 300:
            u[i] = 1.0
    
    # ===== Parameter definition
    grid_shape = (600,600)

    run_experiment(250)
    crear_gif('./Imagenes/2D/','./Imagenes/GIF/2D.gif')
