import threading
import tkinter
from tkinter import ttk

import torch

import sdk
import sv_ttk


class GUI(tkinter.Tk):
    model: sdk.MicrosoftPhi2
    model_options = {}

    def __init__(self):
        super().__init__()

    def load(self):
        """
        Load the model
        """
        self.progress_bar.start(10)
        self.model = sdk.MicrosoftPhi2(**self.model_options)
        self.model.load_model()
        self.progress_bar.stop()
        self.enable_input()

    def generate(self):
        """
        Generate an image from the text in the textbox
        """
        self.progress_bar.start(10)

        # disable generate button & textbox
        self.disable_input()

        conversation = self.model.generate_prompt(prompt=self.textbox.get(), max_new_tokens=300)

        self.textbox.delete(0, tkinter.END)

        generated_text = conversation[0]['generated_text']
        self.conv_label.config(text=generated_text)

        self.enable_input()
        self.progress_bar.stop()

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
        self.title("Demo 1: conversation")  # Changed title

        # Frame for the conversation display
        self.conversation_frame = ttk.Frame(self, width=600, height=400, relief="solid")  # Adjusted dimensions
        self.conversation_frame.pack(padx=10, pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(pady=5)

        self.conv_label = ttk.Label(self.conversation_frame, wraplength=600)  # Added wraplength to handle long text
        self.conv_label.pack(padx=10, pady=10)

        # Textbox for conversation display
        self.textbox = ttk.Entry(self, width=50)
        self.textbox.pack(padx=10, pady=10)

        # Generate button
        self.generate_button = ttk.Button(self, text="Generate", command=self.start_generation)
        self.generate_button.pack(padx=10, pady=10)

        self.disable_input()

        sv_ttk.set_theme("dark")

    def run(self):
        """
        Run the GUI
        """
        # Create and start a new thread to load the model
        loading_thread = threading.Thread(target=self.load)
        self.after(300, lambda: loading_thread.start())

        # Run main loop
        self.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.setup()
    gui.run()