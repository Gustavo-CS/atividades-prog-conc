import random
import threading
import time

def gerar_numeros_aleatorios(n=100, min_val=1, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(n)]

def quicksort_threaded(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    
    left_sorted = []
    right_sorted = []

    def sort_left():
        nonlocal left_sorted
    left_sorted = quicksort_threaded(left)

    def sort_right():
        nonlocal right_sorted
    right_sorted = quicksort_threaded(right)

    left_thread = threading.Thread(target=sort_left)
    right_thread = threading.Thread(target=sort_right)

    left_thread.start()
    right_thread.start()

    left_thread.join()
    right_thread.join()

    return left_sorted + [pivot] + right_sorted

def medir_tempo(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

if __name__ == "__main__":

    numeros = gerar_numeros_aleatorios()
    print("Primeiros 10 números antes da ordenação:", numeros[:10])
    numeros_ordenados, tempo = medir_tempo(quicksort_threaded, numeros)
    print("Primeiros 10 números após a ordenação (paralelizada):", numeros_ordenados[:10])
    print(f"Tempo: {tempo:.5f} segundos")
