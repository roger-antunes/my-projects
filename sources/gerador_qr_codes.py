import qrcode
import os

# Diretório para salvar os QR codes
os.makedirs("qrcodes", exist_ok=True)

# Gera QR codes para IDs de 1 a 70 com 4 orientações
for id_aluno in range(1, 71):
    for resposta in ['A', 'B', 'C', 'D']:
        data = f"{id_aluno}_{resposta}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f"qrcodes/{id_aluno}_{resposta}.png")

print("QR codes gerados com sucesso!")
