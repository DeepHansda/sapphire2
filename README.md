# Sapphire inspired By Stable Diffusion WebUI

This is a personal project inspired by Stable Diffusion WebUI, built to simplify AI-based image generation and editing. This project leverages modern web technologies and powerful AI tools to provide an intuitive interface for creating and managing AI-generated content.

## Notebooks

The following Jupyter notebooks are included in the repository for experimentation and further exploration:

### For Kaggle
1. Click on the following link to open the notebook directly in Kaggle:
[![Run in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/deephansda/sapphire/edit)

### For Google Colab
1. Click on the following link to open the notebook directly in Google Colab:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uZbUHqhutVMMWtsTO_pnve9naC3jcsfq?usp=sharing)

## Features

- **Text-to-Image Generation**: Create unique images from text prompts using pre-trained Stable Diffusion models.
- **Image-to-Image Generation**: Modify existing images based on new prompts, enabling creative edits or transformations.
- **Use SD Models For Generation**: Use different different pretrained SD Models for image Generation.
- **Fast and responsive API** with **FastAPI**.
- **Dynamic and interactive user interface** using **Jinja2** templates.
- **Elegant and modern UI design** with **TailwindCSS**.
- **Easy setup and deployment** for local and production environments.

## Technologies Used

- **FastAPI**: For building the backend and REST API.
- **Diffusers**: To leverage pre-trained Stable Diffusion models for image generation (Text-to-Image and Image-to-Image).
- **Jinja2**: For rendering dynamic HTML templates.
- **TailwindCSS**: For creating a modern, responsive UI.
- **Python**: The primary programming language for the backend and AI logic.


## Installation

Follow these steps to set up and run the project locally or on notebook:

1. Clone the repository:
   ```bash
   git clone https://github.com/DeepHansda/sapphire2
   cd sapphire2
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Install JavaScript Modules:
   ```bash
   cd sapphire2/src/js_modules"

   npm install -g localtunnel
   npm install -g pm2
   npm install
  
  
   npm run build
   pm2 start "npm run dev" --name tailwind-watch
4. Install aria2p for download files:
   ```bash
   
   pip install aria2p
   apt-get install aria2  -y
   aria2c --enable-rpc --rpc-listen-all=true --daemon=true
5. Start App:
   ```bash
   cd sapphire2/src
   python server.py


## Install JavaScript Modules
Follow this steps for install Node modules and start tailwind agent in background:
   
