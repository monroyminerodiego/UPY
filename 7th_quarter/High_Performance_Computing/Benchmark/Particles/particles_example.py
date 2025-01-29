import matplotlib.pyplot as plt
from matplotlib import animation
from random import uniform
import cProfile

class Particle:
    def __init__(self,x,y,vel):
        self.x = x
        self.y = y
        self.vel = vel

class ParticleSimulator:
    def __init__(self,particles:list):
        self.particles = particles

    # @profile #type: ignore
    def evolve(self,dt):
        timestep = 0.00001 #Time Delta
        nsteps = int(dt / timestep)
        for i in range(nsteps):
            for p in self.particles:
                # Calculate r
                r = (p.x**2 + p.y**2)**0.5

                # Calculate speed components
                v_x = - p.vel * p.y / r
                v_y = + p.vel * p.x / r

                # Calculate displacement
                d_x = v_x * timestep
                d_y = v_y * timestep

                # Update new motions
                p.x += d_x
                p.y += d_y

def visualize(simulator):
    ''' '''
    X = [p.x for p in simulator.particles]
    Y = [p.x for p in simulator.particles]

    fig = plt.figure()
    ax = plt.subplot(111,aspect = 'equal')
    line, = ax.plot(X,Y,'ro')
    
    # Axis limits
    plt.xlim(-1,1)
    plt.ylim(-1,1)

    def init():
        line.set_data([],[])
        return line,
    
    def animate(i):
        simulator.evolve(0.01)
        X = [p.x for p in simulator.particles]
        Y = [p.y for p in simulator.particles]

        line.set_data(X,Y)
        return line,

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        interval = 10
    )

    plt.show()

def benchmark():
    particles = [Particle(uniform(-1.0,1.0),uniform(-1.0,1.0),uniform(-1.0,1.0)) for _ in range(100)]
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)


def mostrar_particulas():
    particles = [Particle(uniform(-1.0,1.0),uniform(-1.0,1.0),uniform(-1.0,1.0)) for _ in range(100)]
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)
    visualize(simulator)

if __name__ == '__main__':
    # import os, platform
    # os.system('cls') if platform.system() == 'Windows' else os.system('clear')
    

    # =============== Codigo para medir tiempos
    pr = cProfile.Profile()
    pr.enable()
    benchmark()
    pr.disable()
    pr.print_stats(sort = 'ncalls')
    pr.print_stats(sort = 'tottime')
    pr.print_stats(sort = 'cumtime')

    # =============== Codigo para mostrar particulas
    input('Presiona enter para simular las particulas...')
    mostrar_particulas()