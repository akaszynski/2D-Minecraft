import pyvista as pv
import numpy as np

MOVE = [3, 1, 2, 2, 0, 0, 3, 3, 3, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0]


def ground_level(freq, seed, x_start, x_dim, amp=1, bias=64):
    rng = np.random.default_rng(seed)
    phase = rng.random(3)

    noise = pv.perlin_noise(amp, [freq, 1, 1], phase)

    sampled = pv.sample_function(
        noise,
        bounds=(x_start, x_start + x_dim, 0, 0, 0, 0),
        dim=(x_dim, 1, 1)
    )

    return sampled['scalars'].astype(int) + bias


def perlin_2d(freq, seed, x_start, x_dim, y_dim, amp=1, bias=0):
    rng = np.random.default_rng(seed)
    phase = rng.random(3)

    freq = [freq[0], freq[0], 1]
    noise = pv.perlin_noise(amp, freq, phase)

    sampled = pv.sample_function(
        noise,
        bounds=(x_start, x_start + x_dim, 0, y_dim, 0, 0),
        dim=(x_dim, y_dim, 1)
    )

    return sampled['scalars'] + bias


def blob(x_dim, y_dim, x_start, seed, chunk_num, n=5, max_height=None):

    rng_c = np.random.default_rng()
    dep = rng_c.integers(1, x_dim*y_dim, n)
    dep_sz = rng_c.integers(0, 13, n)

    blob_ind = []
    for index, sz in zip(dep, dep_sz):
        if not sz:
            continue
        blob_ind.append(index)

        for action in MOVE[:sz]:
            if action == 0:  # up
                blob_ind.append(blob_ind[-1] - 1)
            elif action == 1:  # down
                blob_ind.append(blob_ind[-1] + 1)
            elif action == 2:  # left
                blob_ind.append(blob_ind[-1] - x_dim)
            elif action == 3:  # right
                blob_ind.append(blob_ind[-1] + x_dim)

    blob_ind = np.array(blob_ind)
    blob_ind = blob_ind[blob_ind < x_dim*y_dim]
    blob_ind = blob_ind[blob_ind > 0]

    if max_height is not None:
        blob_ind = blob_ind[blob_ind > (y_dim - max_height)*x_dim]

    return set(blob_ind)

    # grid = pyvista.UniformGrid((x_dim + 1, y_dim + 1, 1))

    # data = np.zeros(grid.n_cells, dtype=bool)
    # data[blob_ind] = True

    # grid['data'] = data
    # grid.plot(cpos='xy', cmap='gray')


if __name__ == '__main__':
    case = '1d'

    x_dim = 128
    y_dim = 128
    x_start = 0

    if case == '1d':
        glevel = ground_level(0.1, 0, x_start, x_dim, amp=10, bias=64)
        import matplotlib.pyplot as plt
        plt.plot([0, x_dim], [63, 63])
        plt.step(np.arange(x_dim), glevel)
        plt.ylim(0, y_dim)
        plt.show()
    else:
        import pyvista

        # coal
        freq = (0.3, 0.3)
        scalars = perlin_2d(freq, None, x_start, x_dim, y_dim, amp=1.4, bias=0) > 1
        grid = pyvista.UniformGrid((x_dim + 1, y_dim + 1, 1))
        grid.plot(scalars=scalars, cpos='xy', cmap='gray',
                  show_scalar_bar=False)
