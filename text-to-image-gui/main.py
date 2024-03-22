import threading
import tkinter
from tkinter import ttk
import sdk
import sv_ttk

class Generator(threading.Thread):

    model: sdk.StabilityaiStableDiffusionXlBase1_0

    def __init__(self, image_label):
        super().__init__()
        self.image_label = image_label
        self.model = sdk.StabilityaiStableDiffusionXlBase1_0()

    def run(self):
        # Generate the image
        image = self.generate_image(self.text)

        # Display the image
        self.image_label.configure(image=image)
        self.image_label.image = image

    def generate_image(self, text):
        return self.model.generate_image(text)

class GUI(tkinter.Tk):
    generator: Generator

    def __init__(self):
        super().__init__()

    def generate(self):
        pass

    def setup(self):
        self.title("Demo 1: text to image")

        # Frame for the image placeholder
        # Frame for the image placeholder
        image_frame = ttk.Frame(self, width=300, height=200, relief="solid")
        image_frame.pack(padx=10, pady=10)

        # Placeholder for the image
        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(padx=10, pady=10)

        # Textbox
        textbox = ttk.Entry(self, width=50)
        textbox.pack(padx=10, pady=10)

        # Generate button
        generate_button = ttk.Button(self, text="Generate", command=self.generate)
        generate_button.pack(padx=10, pady=10)

        sv_ttk.set_theme("dark")

        self.generator = Generator(self.image_label)

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.setup()
    gui.run()
