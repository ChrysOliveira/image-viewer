import io

import PySimpleGUI as sg
from PIL import Image


def convert_to_bytes(file_or_bytes):
    img = Image.open(file_or_bytes)
    base_width = 1000
    wpercent = base_width / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


if __name__ == "__main__":

    menu_def = [
        [
            "File",
            [
                "New",
                "Open",
                "Save",
                "Exit",
            ],
        ],
        [
            "Edit",
            [
                "Cut",
                "Copy",
                "Paste",
                "Undo",
            ],
        ],
        [
            "Help",
            [
                "About...",
            ],
        ],
    ]

    layout = [
        [sg.Menu(menu_def)],
        [
            sg.Image(
                key="-IMAGE-",
            )
        ],
    ]

    window = sg.Window("Visualizador de Imagens", layout, resizable=True)

    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == "Open":
            new_image_path = sg.popup_get_file("Selecione a imagem")
            new_imgdata = convert_to_bytes(new_image_path)
            window["-IMAGE-"].update(data=new_imgdata)
            window.refresh()
            window.move_to_center()
