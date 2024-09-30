from fpdf import FPDF
import os

input_folder = '/home/casa/Downloads/QResposta_v1/qrcodes/'
output_file = 'output.pdf'

pdf = FPDF()
imagens = []
for filename in sorted(os.listdir(input_folder)):
    if filename.endswith('.png'):
        img_path = os.path.join(input_folder, filename)
        imagens.append((img_path, filename[:-4].replace('_', ' ')))

# Aumenta o tamanho das imagens em 10% e mais 5% e mais 5%
tamanho_imagem = 110 * 1.1 * 1.05 * 1.05

for i in range(0, len(imagens), 2):
    pdf.add_page()
    if i + 1 < len(imagens):
        pdf.image(imagens[i][0], 40, 20, tamanho_imagem, tamanho_imagem)
        pdf.set_xy(50, 130)
        pdf.set_font("Times", style='B', size=10)  # Adiciona o estilo 'B' para negrito
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, txt=imagens[i][1], ln=True, align='C')
        pdf.image(imagens[i+1][0], 40, 140, tamanho_imagem, tamanho_imagem)
        pdf.set_xy(50, 250)
        pdf.set_font("Times", style='B', size=10)  # Adiciona o estilo 'B' para negrito
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, txt=imagens[i+1][1], ln=True, align='C')
    else:
        pdf.image(imagens[i][0], 40, 20, tamanho_imagem, tamanho_imagem)
        pdf.set_xy(50, 130)
        pdf.set_font("Times", style='B', size=10)  # Adiciona o estilo 'B' para negrito
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, txt=imagens[i][1], ln=True, align='C')

pdf.output(output_file)
