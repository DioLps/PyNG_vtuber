import io
import os
import PySimpleGUI as sg
from PIL import Image
import sounddevice as sd
import numpy as np
from avatar_image import AvatarImage

class MainScreen:
    file_types = [("PNG (*.png)", "*.png")]
    load_avatar_event_label = "Load Avatar"
    reset_button_event_label = "Reset"

    def __init__(self):
        sg.theme('DarkAmber') 
        highlight_image = AvatarImage(
            key = '-HIGHLIGHT_IMAGE-',
            target = '-HIGHLIGHT_IMAGE_TARGET-',
            upload_button_key = '-HIGHLIGHT_IMAGE_BUTTON_KEY-'
        )
        idle_image = AvatarImage(
            key = '-IDLE_IMAGE_IMAGE-',
            target = '-IDLE_IMAGE_TARGET-',
            upload_button_key = '-IDLE_IMAGE_BUTTON_KEY-'
        )
        
        layout = [
            [
                sg.Input(key=idle_image.target, enable_events=True, visible=False),
                sg.FileBrowse(key=idle_image.upload_button_key, button_text='Get idle avatar\'s image',file_types=self.file_types, target=idle_image.target,size=(22,2)),
                sg.Input(key=highlight_image.target, enable_events=True, visible=False),
                sg.FileBrowse(key=highlight_image.upload_button_key, button_text='Get highlight avatar\'s image',file_types=self.file_types, target=highlight_image.target,size=(22,2)),
                sg.Button(self.reset_button_event_label,size=(22,2))
            ],
            [
                sg.Image(key="-IMAGE-",background_color="#00b140")
            ],
        ]
    
        window = sg.Window("PyNG Vtuber", layout, size=(600, 675),resizable=True)
        stream = ""

        def print_sound(indata, outdata, frames, time, status):
            volume_norm = np.linalg.norm(indata)*10
            if int(volume_norm) > 0:
                window["-IMAGE-"].update(data=highlight_image.selected_file)
            else:
                window["-IMAGE-"].update(data=idle_image.selected_file)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break

            if event == self.reset_button_event_label:
                window[highlight_image.upload_button_key].Update(disabled=False)
                window[idle_image.upload_button_key].Update(disabled=False)
                highlight_image.disabled = False
                idle_image.disabled = False
                highlight_image.selected_file = ""
                idle_image.selected_file = ""

            if event == highlight_image.target:
                if os.path.exists(values[highlight_image.target]):
                    image = Image.open(values[highlight_image.target])
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    highlight_image.selected_file = bio.getvalue()
                    window[highlight_image.upload_button_key].Update(disabled=True)
                    highlight_image.disabled = True

            if event == idle_image.target:
                if os.path.exists(values[idle_image.target]):
                    image = Image.open(values[idle_image.target])
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    idle_image.selected_file = bio.getvalue()
                    window[idle_image.upload_button_key].Update(disabled=True)
                    idle_image.disabled = True
            
            if highlight_image.disabled == True and idle_image.disabled == True:
                stream = sd.Stream(callback=print_sound)
                stream.start()

        stream.stop()
        window.close()


