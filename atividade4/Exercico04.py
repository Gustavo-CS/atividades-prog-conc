import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import time
import threading
import multiprocessing


lock = threading.Lock()

# Função para gerar fractais usando um Sistema de Funções Iteradas (IFS)
def gerar_fractal(transformacoes, probabilidades, iteracoes=100000):
    if not abs(sum(probabilidades) - 1.0) < 1e-6:
        raise ValueError("As probabilidades devem somar 1.")
    
    x, y = 0.0, 0.0
    pontos = []

    for _ in range(iteracoes):
        r = random.random()
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                transformacao = transformacoes[i]
                break
        
        x, y = transformacao(x, y)
        pontos.append((x, y))
    
    return pontos

# Triângulo de Sierpinski
def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    probabilidades = [1/3, 1/3, 1/3]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    with lock:
        plt.figure()
        plt.scatter(x_vals, y_vals, s=0.1, color='black', marker='.')
        plt.title("Triângulo de Sierpinski")
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "sierpinski.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Samambaia de Barnsley
def samambaia_barnsley():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    probabilidades = [0.01, 0.85, 0.07, 0.07]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    with lock:
        plt.figure()
        plt.scatter(x_vals, y_vals, s=0.1, color='green', marker='.')
        plt.title("Samambaia de Barnsley")
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "samambaia_barnsley.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Conjunto de Mandelbrot
def mandelbrot(width=800, height=800, max_iter=100):
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            c = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            z = 0.0j
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    with lock:
        plt.figure()
        plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='hot', interpolation='bilinear')
        plt.title("Conjunto de Mandelbrot")
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "mandelbrot.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Conjunto de Julia
def julia(c=-0.7 + 0.27015j, width=800, height=800, max_iter=100):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            z = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    with lock:
        plt.figure()
        plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='twilight_shifted', interpolation='bilinear')
        plt.title("Conjunto de Julia")
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "julia.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Curva de Koch (usando matplotlib)
def koch_curve(order=4, size=300):
    def koch_curve_recursive(points, order):
        if order == 0:
            return points
        new_points = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            new_points.append(p1)
            new_points.append((p1[0] + dx / 3, p1[1] + dy / 3))
            new_points.append((p1[0] + dx / 2 - dy * np.sqrt(3) / 6, p1[1] + dy / 2 + dx * np.sqrt(3) / 6))
            new_points.append((p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3))
        new_points.append(points[-1])
        return koch_curve_recursive(new_points, order - 1)

    points = [(0, 0), (size, 0)]
    points = koch_curve_recursive(points, order)

    x_vals, y_vals = zip(*points)
    with lock:
        plt.figure()
        plt.plot(x_vals, y_vals, color='blue', linewidth=1)
        plt.title("Curva de Koch")
        plt.axis('equal')
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "koch_curve.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Árvore Fractal (usando matplotlib)
def fractal_tree():
    def draw_tree(ax, x, y, length, angle, depth):
        if depth == 0:
            return
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        ax.plot([x, x_end], [y, y_end], color='brown', linewidth=1)
        draw_tree(ax, x_end, y_end, length * 0.7, angle - 30, depth - 1)
        draw_tree(ax, x_end, y_end, length * 0.7, angle + 30, depth - 1)

    with lock:
        fig, ax = plt.subplots()
        draw_tree(ax, 0, 0, 100, 90, 8)
        plt.title("Árvore Fractal")
        plt.axis('equal')
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "fractal_tree.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Tapete de Sierpinski
def sierpinski_carpet(size=3, iterations=4):
    carpet = np.ones((size**iterations, size**iterations))

    def recursive_remove(grid, x, y, size, iteration):
        if iteration == 0:
            return
        sub_size = size // 3
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    grid[x + sub_size:x + 2 * sub_size, y + sub_size:y + 2 * sub_size] = 0
                else:
                    recursive_remove(grid, x + i * sub_size, y + j * sub_size, sub_size, iteration - 1)

    recursive_remove(carpet, 0, 0, size**iterations, iterations)
    with lock:
        plt.figure()
        plt.imshow(carpet, cmap='gray_r')
        plt.title("Tapete de Sierpinski")
        plt.axis('off')
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "sierpinski_carpet.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Esponja de Menger
def menger_sponge(iterations=2):
    def generate_sponge(grid, x, y, z, size, iteration):
        if iteration == 0:
            return
        sub_size = size // 3
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i == 1 and j == 1 or i == 1 and k == 1 or j == 1 and k == 1:
                        continue
                    generate_sponge(grid, x + i * sub_size, y + j * sub_size, z + k * sub_size, sub_size, iteration - 1)

    grid_size = 3**iterations
    grid = np.ones((grid_size, grid_size, grid_size))
    generate_sponge(grid, 0, 0, 0, grid_size, iterations)

    with lock:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(grid, edgecolor='k')
        plt.title("Esponja de Menger")
        plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "menger_sponge.png"), bbox_inches='tight', dpi=300)
        plt.close()
        pass

# Função para gerar todos os fractais
def gerar_todos_fractais_sequencial():
    # print("Gerando Triângulo de Sierpinski...")
    sierpinski()

    # print("Gerando Samambaia de Barnsley...")
    samambaia_barnsley()

    # print("Gerando Conjunto de Mandelbrot...")
    mandelbrot()

    # print("Gerando Conjunto de Julia...")
    julia()

    # print("Gerando Curva de Koch...")
    koch_curve()

    # print("Gerando Árvore Fractal...")
    fractal_tree()

    # print("Gerando Tapete de Sierpinski...")
    sierpinski_carpet()

    # print("Gerando Esponja de Menger...")
    menger_sponge()

def gerar_todos_fractais_multithreading():
    # print("Gerando Triângulo de Sierpinski...")
    sierpinski_thread = threading.Thread(target=sierpinski)
    sierpinski_thread.start()

    # print("Gerando Samambaia de Barnsley...")
    samambaia_barnsley_thread = threading.Thread(target=samambaia_barnsley)
    samambaia_barnsley_thread.start()

    # print("Gerando Conjunto de Mandelbrot...")
    mandelbrot_thread = threading.Thread(target=mandelbrot)
    mandelbrot_thread.start()

    # print("Gerando Conjunto de Julia...")
    julia_thread = threading.Thread(target=julia)
    julia_thread.start()

    # print("Gerando Curva de Koch...")
    koch_curve_thread = threading.Thread(target=koch_curve)
    koch_curve_thread.start()

    # print("Gerando Árvore Fractal...")
    fractal_tree_thread = threading.Thread(target=fractal_tree)
    fractal_tree_thread.start()

    # print("Gerando Tapete de Sierpinski...")
    sierpinski_carpet_thread = threading.Thread(target=sierpinski_carpet)
    sierpinski_carpet_thread.start()

    # print("Gerando Esponja de Menger...")
    menger_sponge_thread = threading.Thread(target=menger_sponge)
    menger_sponge_thread.start()

    sierpinski_thread.join()
    samambaia_barnsley_thread.join()
    mandelbrot_thread.join()
    julia_thread.join()
    koch_curve_thread.join()
    fractal_tree_thread.join()
    sierpinski_carpet_thread.join()
    menger_sponge_thread.join()


def gerar_todos_fractais_multiprocessing():
    processos = [
        multiprocessing.Process(target=sierpinski),
        multiprocessing.Process(target=samambaia_barnsley),
        multiprocessing.Process(target=mandelbrot),
        multiprocessing.Process(target=julia),
        multiprocessing.Process(target=koch_curve),
        multiprocessing.Process(target=fractal_tree),
        multiprocessing.Process(target=sierpinski_carpet),
        multiprocessing.Process(target=menger_sponge),
    ]

    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()

def medir_tempo(func):
    start_time = time.time()
    func()
    end_time = time.time()
    return end_time - start_time

# Executa a geração de todos os fractais
if __name__ == "__main__":
    tempo = medir_tempo(gerar_todos_fractais_sequencial)
    print(f"Tempo Sequencial: {tempo:.5f} segundos")
    tempo2 = medir_tempo(gerar_todos_fractais_multithreading)
    print(f"Tempo multithread: {tempo2:.5f} segundos")
    tempo3 = medir_tempo(gerar_todos_fractais_multiprocessing)
    print(f"Tempo multiprocessing: {tempo3:.5f} segundos")