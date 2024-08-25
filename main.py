import PySimpleGUI as sg
from PIL import Image, ExifTags
import io
import os
import webbrowser

image_atual = None
image_path = None
image_base_width = 1000

def gera_link_localizacao_foto(latitude_ref, latitude, longitude_ref, longitude):
    lat_multiplicador = 1.0
    if latitude_ref == "S":
        lat_multiplicador = -1.0

    log_multiplicador = 1.0
    if longitude_ref == "W":
        log_multiplicador = -1.0

    latitude_decimal = lat_multiplicador * (latitude[0] + latitude[1]/60 + latitude[2]/3600)
    longitude_decimal = log_multiplicador * (longitude[0] + longitude[1]/60 + longitude[2]/3600)

    link_maps = f"https://www.google.com/maps/@{latitude_decimal},{longitude_decimal},18z"

    return link_maps

def exif_data():
    global image_atual

    exif_data = ""
    exif_table = {}

    for tag, value in image_atual._getexif().items():
        decoded = ExifTags.TAGS.get(tag)
        exif_table[decoded] = value

    gps_info = {}

    for key in exif_table['GPSInfo'].keys():
        decode = ExifTags.GPSTAGS.get(key, key)
        gps_info[decode] = exif_table['GPSInfo'][key]

    exif_table.pop('GPSInfo')

    for key, value in exif_table.items():
        exif_data += f"{key}: {value}\n"

    for key, value in gps_info.items():
        exif_data += f"{key}: {value}\n"

    link_maps = gera_link_localizacao_foto(gps_info['GPSLatitudeRef'], gps_info['GPSLatitude'],gps_info['GPSLongitudeRef'],gps_info['GPSLongitude'])

    webbrowser.open(link_maps, new=0, autoraise=True)

    sg.popup("Dados EXIF: ", exif_data)


def resize_image(img):
    global image_base_width

    wpercent = image_base_width / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((image_base_width, hsize), Image.Resampling.LANCZOS)
    return img


def open_image(filename):
    global image_atual
    global image_path
    image_path = filename
    image_atual = Image.open(filename)

    resized_img = resize_image(image_atual)
    # Converte a image PIL para o formato que o PySimpleGUI
    img_bytes = io.BytesIO()  # Permite criar objetos semelhantes a arquivos na memória RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())


def save_image(filename):
    global image_path
    if image_path:
        image_atual = Image.open(image_path)
        with open(filename, 'wb') as file:
            image_atual.save(file)


def info_image():
    global image_atual
    global image_path
    global image_base_width

    if image_atual:
        largura, altura = image_atual.size
        formato = image_atual.format
        tamanho_bytes = os.path.getsize(image_path)
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")


layout = [
    [sg.Menu([
        ['Arquivo', ['Abrir', 'Salvar', 'Fechar']],
        ['Sobre a image', ['Informacoes', 'Exif data']],
        ['Sobre', ['Desenvolvedor']]
    ])],
    [sg.Image(key='-IMAGE-', size=(image_base_width, 600))],
]

window = sg.Window('', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar imagem')
        if arquivo:
            open_image(arquivo)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True,
                                        file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
    elif event == 'Exif data':
        exif_data()
    elif event == 'Desenvolvedor':
        sg.popup('Chrystian Oliveira')

window.close()