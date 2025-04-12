import numpy as np
from mpi4py import MPI

if __name__ == "__main__":
    world_comm = MPI.COMM_WORLD
    world_size = world_comm.Get_size()
    my_rank = world_comm.Get_rank()

    N = 10000000
    workloads = [N // world_size + (1 if i < N % world_size else 0) for i in range(world_size)]
    my_start = sum(workloads[:my_rank])
    my_end = my_start + workloads[my_rank]

    a = np.ones(workloads[my_rank])
    b = np.array([1.0 + i for i in range(my_start, my_end)])

    a += b
    local_sum = np.sum(a)
    global_sum = world_comm.reduce(local_sum, op=MPI.SUM, root=0)

    if my_rank == 0:
        average = global_sum / N
        print(f"Average: {average}")
