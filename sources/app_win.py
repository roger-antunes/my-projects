import cv2
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import pygame
import os
import sys
import signal

# Inicializa Pygame para tocar som
pygame.mixer.init()

def atualizar_botoes():
    btn_proxima.config(state=tk.NORMAL if questao_atual < len(questao_df) else tk.DISABLED)

# Carrega o som
def carregar_som():
    try:
        pygame.mixer.music.load("som.mp3")
    except pygame.error:
        messagebox.showwarning("Aviso", "Arquivo de audio, som.mp3 não identificado!")
        return False
    return True

som_carregado = carregar_som()

# Inicializa a janela principal
root = tk.Tk()
root.title("Sistema de coleta de respostas por QRcode - v1 set/2024 - Prof. Roger")

# Cria um Notebook (abas)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Aba 1 - Questões
aba_questao = ttk.Frame(notebook)
notebook.add(aba_questao, text="Questões")

# Configurações da câmera
cap = cv2.VideoCapture(0)

# Variáveis globais
questao_atual = 1
alunos_respostas = {}
questao_df = None
respostas_salvas = {}
flip_camera = tk.BooleanVar(value=False)

# Frame com scrollbar para a questão
questao_frame = tk.Frame(aba_questao)
questao_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

questao_scroll = tk.Scrollbar(questao_frame)
questao_scroll.pack(side=tk.RIGHT, fill=tk.Y)

questao_canvas = tk.Canvas(questao_frame, yscrollcommand=questao_scroll.set)
questao_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

questao_scroll.config(command=questao_canvas.yview)

questao_content = tk.Frame(questao_canvas)
questao_canvas.create_window((0, 0), window=questao_content, anchor='nw')

# Centraliza o conteúdo da aba
questao_content.grid_rowconfigure(0, weight=1)
questao_content.grid_columnconfigure(0, weight=1)

# Label para mostrar a questão atual
lbl_questao = tk.Label(questao_content, text="", font=("Helvetica", 30), anchor='center')
lbl_questao.pack(pady=20)

# Labels para alternativas
lbl_alternativa_a = tk.Label(questao_content, text="", font=("Helvetica", 25), anchor='center')
lbl_alternativa_a.pack(pady=5)

lbl_alternativa_b = tk.Label(questao_content, text="", font=("Helvetica", 25), anchor='center')
lbl_alternativa_b.pack(pady=5)

lbl_alternativa_c = tk.Label(questao_content, text="", font=("Helvetica", 25), anchor='center')
lbl_alternativa_c.pack(pady=5)

lbl_alternativa_d = tk.Label(questao_content, text="", font=("Helvetica", 25), anchor='center')
lbl_alternativa_d.pack(pady=5)

def finalizar_e_gerar_relatorio():
    caminho = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if caminho:
        relatorio_df = pd.DataFrame.from_dict(alunos_respostas, orient='index')
        relatorio_df.drop(columns=['Respondido', 'Label'], inplace=True, errors='ignore')  # Remove 'Respondido' e 'Label'
        relatorio_df['Media Acertos'] = relatorio_df['Acertos'] / len(questao_df) * 100
        relatorio_df.to_excel(caminho)
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

def fechar_aplicacao():
    global captura_ativa
    captura_ativa = False
    if after_id is not None:
        root.after_cancel(after_id)
    try:
        cap.release()  # Libera a câmera
        cv2.destroyAllWindows()  # Fecha todas as janelas do OpenCV
        pygame.mixer.quit()  # Fecha o mixer do Pygame
        root.destroy()  # Fecha o programa
    except Exception as e:
        print(f"Erro ao fechar o programa: {e}")

root.protocol("WM_DELETE_WINDOW", fechar_aplicacao)

btn_frame = tk.Frame(questao_content)
btn_frame.pack(pady=5)

btn_proxima = tk.Button(btn_frame, text="Próxima Questão", command=lambda: proxima_questao(), font=("Helvetica", 15))
btn_proxima.pack(side=tk.LEFT, padx=5)

btn_finalizar = tk.Button(btn_frame, text="Finalizar e Gerar Relatório", command=finalizar_e_gerar_relatorio, font=("Helvetica", 15))
btn_finalizar.pack(side=tk.LEFT, padx=5)

btn_fechar = tk.Button(btn_frame, text="Fechar", command=fechar_aplicacao, font=("Helvetica", 15))
btn_fechar.pack(side=tk.LEFT, padx=5)

# Aba 2 - Alunos e Câmera
aba_alunos_camera = ttk.Frame(notebook)
notebook.add(aba_alunos_camera, text="Alunos e Câmera")

frame_alunos_camera = tk.Frame(aba_alunos_camera)
frame_alunos_camera.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_alunos = tk.Frame(frame_alunos_camera)
frame_alunos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

lbl_camera = tk.Label(frame_alunos_camera)
lbl_camera.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

alunos_respostas = {}

def mostrar_questao():
    global questao_atual
    if questao_df is not None and questao_atual <= len(questao_df):
        questao_info = questao_df.iloc[questao_atual - 1]
        lbl_questao.config(text=f"{questao_info['Número']}) {questao_info['Questão']}")
        lbl_alternativa_a.config(text=f"A) {questao_info['A']}")
        lbl_alternativa_b.config(text=f"B) {questao_info['B']}")
        lbl_alternativa_c.config(text=f"C) {questao_info['C']}")
        lbl_alternativa_d.config(text=f"D) {questao_info['D']}")
        respostas_salvas[questao_info['Número']] = questao_info['Resposta']
        atualizar_botoes()

def carregar_planilhas():
    global alunos_respostas, questao_df
    
    arquivo_alunos = filedialog.askopenfilename(title="Carregar Planilha de Alunos", filetypes=[("Excel files", "*.xlsx")])
    if arquivo_alunos:
        alunos_df = pd.read_excel(arquivo_alunos)
        alunos_respostas = {row['ID']: {'Nome': row['Nome'].split()[0], 'Respondido': False, 'Acertos': 0, 'Label': None} for _, row in alunos_df.iterrows()}
        atualizar_lista_alunos()

    arquivo_questoes = filedialog.askopenfilename(title="Carregar Planilha de Questões", filetypes=[("Excel files", "*.xlsx")])
    if arquivo_questoes:
        questao_df = pd.read_excel(arquivo_questoes)

    mostrar_questao()

def atualizar_lista_alunos():
    for widget in frame_alunos.winfo_children():
        widget.destroy()

    colunas = 3
    alunos_ids = list(alunos_respostas.keys())
    
    for index, id_aluno in enumerate(alunos_ids):
        coluna_index = index % colunas
        if coluna_index == 0:
            row_frame = tk.Frame(frame_alunos)
            row_frame.pack(side=tk.TOP, fill=tk.X)
        
        aluno_label = tk.Label(row_frame, text=f"{id_aluno}: {alunos_respostas[id_aluno]['Nome']}", font=("Helvetica", 15))
        aluno_label.pack(side=tk.LEFT, padx=10, pady=2)
        alunos_respostas[id_aluno]['Label'] = aluno_label

carregar_planilhas()

chk_flip = tk.Checkbutton(aba_alunos_camera, text="Flip Câmera", variable=flip_camera)
chk_flip.pack(side=tk.TOP, pady=5)

# Seleciona câmeras disponíveis
def listar_cameras():
    index = 0
    cameras = []
    while True:
        cap_test = cv2.VideoCapture(index)
        if not cap_test.isOpened():
            break
        cameras.append(f"Câmera {index}")
        cap_test.release()
        index += 1
    return cameras

# Cria combobox para selecionar a câmera
cameras_disponiveis = listar_cameras()
combo_cameras = ttk.Combobox(aba_alunos_camera, values=cameras_disponiveis, state="readonly")
combo_cameras.set("Câmera 0")  # Câmera padrão
combo_cameras.pack(side=tk.TOP, pady=5)

camera_height = 200
lbl_camera.config(height=camera_height)

captura_ativa = True

captura_ativa = True
after_id = None

def processar_frame():
    global captura_ativa
    global after_id
    if not captura_ativa:
        return
    
    global questao_atual
    ret, frame = cap.read()
    if not ret:
        return
    
    if flip_camera.get():
        frame = cv2.flip(frame, 1)

    decoded_objects = decode(frame)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        
        try:
            id_aluno, resposta = data.split('_')
            id_aluno = int(id_aluno)

            if id_aluno in alunos_respostas and not alunos_respostas[id_aluno]['Respondido']:
                alunos_respostas[id_aluno]['Respondido'] = True

                if alunos_respostas[id_aluno]['Label'] is not None:
                    alunos_respostas[id_aluno]['Label'].config(bg='lightblue')

                if som_carregado and not pygame.mixer.music.get_busy(): 
                    pygame.mixer.music.play()

                if resposta == respostas_salvas[questao_atual]:
                    alunos_respostas[id_aluno]['Acertos'] += 1

                print(f"ID: {id_aluno}, Resposta: {resposta}")
        except ValueError:
            print(f"Formato inválido: {data}")

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    imgtk = ImageTk.PhotoImage(image=img_pil)
    lbl_camera.imgtk = imgtk
    lbl_camera.configure(image=imgtk)

    if captura_ativa:
        after_id = root.after(10, processar_frame)


def proxima_questao():
    global questao_atual
    for id_aluno in alunos_respostas:
        alunos_respostas[id_aluno]['Respondido'] = False

    questao_atual += 1
    if questao_atual > len(questao_df):
        questao_atual = len(questao_df)  # Não ultrapassa a última questão
    mostrar_questao()

    for id_aluno in alunos_respostas:
        if alunos_respostas[id_aluno]['Label'] is not None:
            alunos_respostas[id_aluno]['Label'].config(bg='white')

processar_frame()
root.mainloop()

cap.release()
