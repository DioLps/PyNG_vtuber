class AvatarImage:
    def __init__(self, key, target, upload_button_key):
        self.key = key
        self.target = target
        self.upload_button_key = upload_button_key
        self.selected_file = ""
        self.disabled = False