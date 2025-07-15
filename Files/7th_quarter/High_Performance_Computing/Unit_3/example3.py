import numpy as np
from mpi4py import MPI
import time

def minimum_image_distance(r_i, r_j, box_length):
    delta = r_i - r_j
    delta -= box_length * np.round(delta / box_length)
    return np.dot(delta, delta)

def lennard_jones_potential(r2):
    inv_r6 = (1.0 / r2) ** 3
    return 4.0 * inv_r6 * (inv_r6 - 1.0)

def compute_local_energy(coordinates, box_length, cutoff2, comm):
    num_particles = len(coordinates)
    rank = comm.Get_rank()
    size = comm.Get_size()
    local_energy = 0.0

    for i_particle in range(rank, num_particles, size):
        i_position = coordinates[i_particle]
        e_total = 0.0
        for j in range(num_particles):
            if i_particle != j:
                rij2 = minimum_image_distance(i_position, coordinates[j], box_length)
                if rij2 < cutoff2:
                    e_total += lennard_jones_potential(rij2)
        local_energy += e_total

    return local_energy

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Parámetros de la simulación
    num_particles = 100
    box_length = 10.0
    cutoff = 3.0
    cutoff2 = cutoff ** 2
    num_steps = 500
    displacement = 0.1

    np.random.seed(42 + rank)
    coordinates = np.random.rand(num_particles, 3) * box_length

    if rank == 0:
        start_time = time.time()
        energies = []

    for step in range(1, num_steps + 1):
        if rank == 0:
            i_particle = np.random.randint(num_particles)
            old_position = coordinates[i_particle].copy()
            displacement_vector = (np.random.rand(3) - 0.5) * displacement
            coordinates[i_particle] += displacement_vector
            coordinates[i_particle] %= box_length

        # Broadcast coordenadas actualizadas
        coordinates = comm.bcast(coordinates, root=0)

        # Calcular energía nueva
        local_energy_new = compute_local_energy(coordinates, box_length, cutoff2, comm)
        total_energy_new = comm.reduce(local_energy_new, op=MPI.SUM, root=0)

        if rank == 0:
            # Volver a estado anterior para evaluar energía vieja
            coordinates[i_particle] = old_position
            coordinates = comm.bcast(coordinates, root=0)

        # Calcular energía anterior
        local_energy_old = compute_local_energy(coordinates, box_length, cutoff2, comm)
        total_energy_old = comm.reduce(local_energy_old, op=MPI.SUM, root=0)

        if rank == 0:
            delta_e = total_energy_new - total_energy_old
            if delta_e < 0 or np.random.rand() < np.exp(-delta_e):
                # Aceptar cambio
                coordinates[i_particle] = (old_position + displacement_vector) % box_length
            else:
                # Rechazar cambio
                coordinates[i_particle] = old_position

            if step % 50 == 0:
                print(f"Step {step} | Energy: {total_energy_new:.4f}")
                energies.append((step, total_energy_new))

    if rank == 0:
        end_time = time.time()
        print(f"\nSimulation completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
