from PIL import Image
from tkinter import Tk, filedialog
import threading

def converter_faixa(imagem, inicio, fim, resultado, index):
    largura, altura = imagem.size
    faixa = Image.new("L", (largura, fim - inicio))

    for x in range(largura):
        for y in range(inicio, fim):
            r, g, b = imagem.getpixel((x, y))
            luminancia = int(0.299 * r + 0.587 * g + 0.114 * b)
            faixa.putpixel((x, y - inicio), luminancia)

    resultado[index] = faixa

def converter_para_pb_threads():
    try:
        root = Tk()
        root.withdraw()

        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_imagem:
            print("Nenhuma imagem foi selecionada.")
            return

        imagem = Image.open(caminho_imagem).convert("RGB")
        largura, altura = imagem.size

        num_threads = 4  # Defina o número de threads desejado
        threads = []
        resultado = [None] * num_threads
        faixa_altura = altura // num_threads

        for i in range(num_threads):
            inicio = i * faixa_altura
            fim = altura if i == num_threads - 1 else (i + 1) * faixa_altura
            thread = threading.Thread(target=converter_faixa, args=(imagem, inicio, fim, resultado, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        imagem_pb = Image.new("L", (largura, altura))
        for i, faixa in enumerate(resultado):
            imagem_pb.paste(faixa, (0, i * faixa_altura))

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar imagem em preto e branco",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_saida:
            print("Operação de salvamento cancelada.")
            return

        imagem_pb.save(caminho_saida)
        print(f"Imagem convertida com sucesso! Salva em: {caminho_saida}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    converter_para_pb_threads()