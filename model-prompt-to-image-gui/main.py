import threading
import tkinter
from tkinter import ttk

import torch

import sdk
import sv_ttk

from PIL import ImageTk


class GUI(tkinter.Tk):
    img_model: sdk.StabilityaiStableDiffusionXlBase10
    img_model_options = {
        'torch_dtype': torch.float16,
        'use_safetensors': True,
        'add_watermarker': False,
        'variant': "fp16"
    }
    txt_model: sdk.Fredzhang7AnimeAnythingPromptgenV2
    txt_model_options = {
    }
    model_manager_img = sdk.ModelsManagement()
    model_manager_txt = sdk.ModelsManagement()

    def __init__(self):
        super().__init__()
        self.bind('<Return>', lambda event: self.start_generation())
        self.image_output_event = threading.Event()

    def load_img(self):
        """
        Load the models
        """

        self.progress_bar.start(10)
        self.img_model = sdk.StabilityaiStableDiffusionXlBase10(**self.img_model_options)
        self.model_manager_img.add_model(new_model=self.img_model)
        self.model_manager_img.load_model(self.img_model.model_name)
        self.image_output_event.set()


    def load_txt(self):
        self.progress_bar.start(10)
        self.txt_model = sdk.Fredzhang7AnimeAnythingPromptgenV2(**self.txt_model_options)
        self.txt_model.create_pipeline()
        self.model_manager_txt.add_model(new_model=self.txt_model)
        self.model_manager_txt.load_model(self.txt_model.model_name)
        self.progress_bar.stop()
        self.enable_input()

    def generate(self):
        """
        Generate an image from the text in the textbox
        """
        self.progress_bar.start(10)

        # disable generate button & textbox
        self.disable_input()
        prompt = " Instruct: " + self.textbox.get() + ".\nOutput:"

        conversation = self.model_manager_txt.generate_prompt(prompt=prompt, max_length=76,
                                                              num_return_sequences=1, do_sample=True,
                                                              repetition_penalty=1.2, temperature=0.7, top_k=4,
                                                              early_stopping=True, num_beams=20,
                                                              truncation=True,model_name = self.txt_model.model_name)
        generated_text = conversation[0]['generated_text']

        # Update the conversation label with the generated text
        self.conv_label.config(text=generated_text)

        self.textbox.delete(0, tkinter.END)
        self.progress_bar.stop()

        self.progress_bar.start(10)
        self.run_img()
        output = generated_text.split('\nOutput: ')[1]

        img = self.model_manager_img.generate_prompt(prompt=output, height=512, width=512)[0]

        tkimg = ImageTk.PhotoImage(img[0])
        self.image_label.config(image=tkimg)
        self.image_label.image = tkimg
        self.image_output_event.wait()
        self.progress_bar.stop()
        self.enable_input()

    def start_generation(self):
        """
        Start the generation process in a new thread
        """
        generation_thread = threading.Thread(target=self.generate)
        self.after(300, lambda: generation_thread.start())

    def disable_input(self):
        """
        Disable the input fields
        """
        self.generate_button.config(state="disabled")
        self.textbox.config(state="disabled")

    def enable_input(self):
        """
        Enable the input fields
        """
        self.generate_button.config(state="normal")
        self.textbox.config(state="normal")

    def setup(self):
        """
        Setup the GUI
        """
        self.title("Demo 3: text prompt to image")

        # Adjusting dimensions of the main application window
        self.geometry("1200x800")  # Adjusted dimensions

        # Frame for the conversation display
        self.conversation_frame = ttk.Frame(self, width=1000, height=400, relief="solid")  # Adjusted dimensions
        self.conversation_frame.pack(padx=10, pady=10)

        self.conv_label = ttk.Label(self.conversation_frame, wraplength=1000,
                                    anchor='center')  # Added wraplength and anchor
        self.conv_label.pack(padx=10, pady=10)

        # Frame for the image placeholder
        self.image_frame = ttk.Frame(self, width=1000, height=400, relief="solid")  # Adjusted dimensions
        self.image_frame.pack(padx=10, pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(pady=5)

        # Label asking for input
        self.input_label = ttk.Label(self, text="Enter your text prompt:", anchor='center')  # Added anchor
        self.input_label.pack(padx=10, pady=5)

        # Placeholder for the image
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)

        # Textbox
        self.textbox = ttk.Entry(self, width=50)
        self.textbox.pack(padx=10, pady=10)

        # Generate button
        self.generate_button = ttk.Button(self, text="Generate", command=self.start_generation)
        self.generate_button.pack(padx=10, pady=10)

        self.disable_input()

        sv_ttk.set_theme("dark")

    def run_txt(self):
        """
        Run the GUI
        """
        # Create and start a new thread to load the model
        loading_thread = threading.Thread(target=self.load_txt())
        self.after(300, lambda: loading_thread.start())

        # Run main loop
        self.mainloop()

    def run_img(self):
        """
        Run the GUI
        """
        # Create and start a new thread to load the model
        loading_thread = threading.Thread(target=self.load_img())
        self.after(300, lambda: loading_thread.start())


if __name__ == '__main__':
    gui = GUI()
    gui.setup()
    gui.run_txt()