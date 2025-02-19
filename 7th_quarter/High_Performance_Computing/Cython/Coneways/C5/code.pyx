import numpy as np
cimport numpy as cnp

cdef int[:, :] compute_neighbors(cnp.ndarray[int, ndim=2] lattice, int rows, int cols):
    """Calcula la cantidad de vecinos para cada celda."""
    cdef int[:, :] neighbors = np.zeros((rows, cols), dtype=np.int32)
    cdef int i, j, di, dj, ni, nj

    for i in range(rows):
        for j in range(cols):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue  # Omitir la celda actual
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors[i, j] += lattice[ni, nj]

    return neighbors


def update(cnp.ndarray[int, ndim=2] lattice):
    """Actualiza el estado del autómata celular basado en la cantidad de vecinos."""
    cdef int rows = lattice.shape[0]
    cdef int cols = lattice.shape[1]
    cdef int[:, :] neighbors = compute_neighbors(lattice, rows, cols)
    cdef cnp.ndarray[int, ndim=2] new_lattice = np.zeros((rows, cols), dtype=np.int32)
    cdef int i, j

    for i in range(rows):
        for j in range(cols):
            if (neighbors[i, j] == 3) or (lattice[i, j] == 1 and neighbors[i, j] == 2):
                new_lattice[i, j] = 1

    return new_lattice
