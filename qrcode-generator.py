import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont


def add_label_under_qr(image, label, font_path="arial.ttf", font_size=50):
    # Estimativa da altura do texto baseada no tamanho da fonte
    # Esta é uma aproximação; a altura real pode variar dependendo da fonte específica
    text_height_estimated = int(font_size * 1.2)

    # Cria uma nova imagem com espaço extra para o texto abaixo do QR Code
    width, height = image.size
    new_image = Image.new("RGB", (width, height + text_height_estimated + 10), "white")  # +10 para um pouco de espaço extra
    new_image.paste(image, (0, 0))

    # Cria um objeto draw para desenhar na nova imagem
    draw = ImageDraw.Draw(new_image)

    # Tenta carregar a fonte especificada ou usa a padrão se falhar
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        print("caiu")
        font = ImageFont.load_default()

    # Calcula a posição do texto para centralizá-lo abaixo do QR Code
    text_width = draw.textlength(label, font=font)  # Usa textlength para obter a largura do texto
    text_x = (width - text_width) / 2
    text_y = height + 5  # 5 pixels de espaço acima do texto

    # Desenha o texto na imagem
    draw.text((text_x, text_y), label, fill="black", font=font)

    return new_image

# Carregar a planilha CSV
df = pd.read_csv('input.csv')

for index, row in df.iterrows():
    url = row['url']  # Substitua pela coluna com a URL
    label = row['label']  # Substitua pela coluna com o rótulo

    # Gerar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Inserir logo no centro do QR Code
    logo_path = 'logo.png'  # Ajuste para o caminho da sua logo
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = 150  # Ajuste conforme a necessidade
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Calcular posição para a logo
    pos = ((img_qr.size[0] - logo.size[0]) // 2, (img_qr.size[1] - logo.size[1]) // 2)
    img_qr.paste(logo, pos, logo)
    
    # Adicionar rótulo na parte inferior do QR Code
    final_img = add_label_under_qr(img_qr, label)

    # Salvar o QR Code com logo e rótulo
    final_img.save(f'qr_code_{index}.png')

print("QR Codes com logos e rótulos gerados com sucesso!")
