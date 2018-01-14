import multiprocessing as mp
import time
from functools import wraps

import numpy as np
import matplotlib.pyplot as plt


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(f'{t2 - t1} seconds elapsed')
        return res
    return wrapper


def mandelbrot(c, max_iterations=400):
    """Determine number of iterations to divergence in Mandelbrot set.

    Parameters
    ----------
    c : complex
        Complex number to be used in f(z) = z^2 + c
    max_iterations : int
        Maximum iterations; used for testing divergence

    Returns
    -------
    int

        Number of iterations it took for f(z) to diverge, or 0 if it didn't
        diverge within `max_iterations` iterations

    """
    z = c
    for i in range(max_iterations):
        if abs(z) > 2:
            return i
        z = z*z + c
    return 0


@timeit
def mandelbrot_serial(xmin, xmax, ymin, ymax, N=100):
    """Generate image of the Mandelbot set in serial.

    Parameters
    ----------
    xmin : float
        Minimum value of Re[z] to display in image
    xmax : float
        Maximum value of Re[z] to display in image
    ymin : float
        Minimum value of Im[z] to display in image
    ymax : float
        Maximum value of Im[z] to display in image
    N : int
        Number of pixels in each dimension

    Returns
    -------
    numpy.ndarray
        Image of Mandelbrot set of shape (N, N)

    """
    image = np.empty((N, N))
    for i, y in enumerate(np.linspace(ymax, ymin, N)):
        for j, x in enumerate(np.linspace(xmin, xmax, N)):
            image[i, j] = mandelbrot(complex(x, y))
    return image


def process_chunk(queue, xs, ys):
    image = np.empty((ys.size, xs.size))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            image[i, j] = mandelbrot(complex(x, y))

    p = mp.current_process()
    queue.put((p.name, image))


@timeit
def mandelbrot_static(xmin, xmax, ymin, ymax, N=100):
    """Generate image of the Mandelbot set in parallel with static work
    distribution.

    Parameters
    ----------
    xmin : float
        Minimum value of Re[z] to display in image
    xmax : float
        Maximum value of Re[z] to display in image
    ymin : float
        Minimum value of Im[z] to display in image
    ymax : float
        Maximum value of Im[z] to display in image
    N : int
        Number of pixels in each dimension

    Returns
    -------
    numpy.ndarray
        Image of Mandelbrot set of shape (N, N)

    """
    ncpus = mp.cpu_count()

    xs = np.linspace(xmin, xmax, N)
    ys = np.linspace(ymax, ymin, N)

    procs = []

    queue = mp.Queue()
    idx = np.linspace(0, N, ncpus + 1, dtype=int)
    for jmin, jmax in zip(idx[:-1], idx[1:]):
        p = mp.Process(target=process_chunk,
                       args=(queue, xs, ys[jmin:jmax]))
        p.start()

    chunks = dict(queue.get() for i in range(ncpus))
    image = np.vstack(chunks[f'Process-{i+1}'] for i in range(ncpus))

    return image


@timeit
def mandelbrot_dynamic(xmin, xmax, ymin, ymax, N=100):
    """Generate image of the Mandelbot set in parallel with dynamic load balancing.

    Parameters
    ----------
    xmin : float
        Minimum value of Re[z] to display in image
    xmax : float
        Maximum value of Re[z] to display in image
    ymin : float
        Minimum value of Im[z] to display in image
    ymax : float
        Maximum value of Im[z] to display in image
    N : int
        Number of pixels in each dimension

    Returns
    -------
    numpy.ndarray
        Image of Mandelbrot set of shape (N, N)

    """
    xs = np.linspace(xmin, xmax, N)
    ys = np.linspace(ymax, ymin, N)

    with mp.Pool() as pool:
        zs = [complex(x, y) for y in ys for x in xs]
        image = np.array(pool.map(mandelbrot, zs, chunksize=N//4))
        image.shape = (N, N)

    return image


def main():
    xmin = -0.9187
    xmax = -0.9140
    ymin = 0.2744
    ymax = 0.2797
    N = 300

    image1 = mandelbrot_serial(xmin, xmax, ymin, ymax, N)
    image2 = mandelbrot_static(xmin, xmax, ymin, ymax, N)
    image3 = mandelbrot_dynamic(xmin, xmax, ymin, ymax, N)

    assert np.all(image1 == image2), 'Serial/parallel images are different'
    assert np.all(image2 == image3), 'Static/dynamic images are different'

    plt.imshow(image1, cmap='gist_ncar')
    plt.savefig('Mandelbrot.png')


if __name__ == '__main__':
    main()
