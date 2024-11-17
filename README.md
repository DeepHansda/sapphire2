# Sapphire inspired By Stable Diffusion WebUI

A web-based application inspired by Stable Diffusion WebUI, built to simplify AI-based image generation and editing. This project leverages modern web technologies and powerful AI tools to provide an intuitive interface for creating and managing AI-generated content.

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
   
