[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1HLMKyHIk-Z7jpr0slUPqCMbKwVAl-PSe?usp=sharing)
# Extrator de informações de CNH

## Ambiente
Há um [notebook](https://colab.research.google.com/drive/1HLMKyHIk-Z7jpr0slUPqCMbKwVAl-PSe?usp=sharing) no Google Colab disponível para acesso rápido a um ambiente funcional

Para instalar localmente, primeiramente é necessário instalar o Tesseract-OCR

Linux:
```bash
sudo apt install tesseract-ocr
```
Windows:

https://github.com/UB-Mannheim/tesseract/wiki

Feito isso é só instalar os requisitos

```bash
pip install -r requirements.txt
```
## Dataset
Para gerar um dataset randômico de CNHs, basta executar
```bash
cd dataset
python generate_fake_dataset.py
```
Esse script aceita 2 argumentos, sendo eles

```bash
# Quantidade de exemplares a serem gerados (default=10)
python generate_fake_dataset.py --size 10

# E se deseja ou não adicionar ruído aleatório nas imagens (default=False)
python generate_fake_dataset.py --noise False
```
## Extração
Para extrair informações de uma imagem, basta executar
```bash
python cnhextractor.py --image PATH_TO_IMAGE
```
