from mpi4py import MPI

if __name__ == "__main__":
    world_comm = MPI.COMM_WORLD
    world_size = world_comm.Get_size()
    my_rank = world_comm.Get_rank()
    print(f"World Size: {world_size}   Rank: {my_rank}")
