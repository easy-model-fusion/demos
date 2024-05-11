# EMF Project demos

This repository contains some examples of EMF projects.
Any of the projects are created with the emf-cli.

## Run

To run the projects, you need to have the `emf-cli` installed - see [How to install emf-cli](https://easy-model-fusion.github.io/docs/).

Walk to the folder of the project you want to run and execute the following command:

```bash
emf-cli tidy
```

This will install the missing dependencies and models.

You then have two options to run the project:

1. Run the project using python venv
    Bind the python venv
    ```bash
    source .venv/bin/activate
    ```
   Then run the project
    ```bash
    python main.py
    ```
2. Build the project and run it
    ```bash
    emf-cli build
    ```
   This will generate an executable file in the `dist` folder. Check docs for more information.

## Demo 1: Simple GUI to generate stable diffusion images

This demo is a simple GUI app that contains a prompt, a button, and an image.
The prompt asks the user to enter some text, and the button generates a diffusion image with the text entered.

The model used is `stabilityai/stable-diffusion-xl-base-1.0` available [here](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0).

## Demo 3: Simple GUI to generate stable diffusion images from a generated prompt

This demo is also a simple GUI app that contains a prompt, a button, and an image.

It allows users to generate a text prompt for an image using the `FredZhang7/anime-anything-promptgen-v2` available [here](<https://huggingface.co/FredZhang7/anime-anything-promptgen-v2>), the output is then fed to the  `stabilityai/stable-diffusion-xl-base-1.0` available [here](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) for an image generation.
