[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1HLMKyHIk-Z7jpr0slUPqCMbKwVAl-PSe?usp=sharing)
# Extrator de informações de CNH - Teste Docket - Machine Learning

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
## Planejamento
Assim que recebi o projeto, fui para a internet pesquisar abordagens que eu poderia utilizar, bem como quais dados tinham à minha disposição. 

Comecei a anotar as ideias em uma folha de papel e também desenhar qual seria mais ou menos o fluxo que eu iria adotar. Descartei algumas alternativas como usar EAST para a detecção de texto ou usar muitas variantes de imagens no dataset por motivo de tempo. Optei por tentar encontrar ROIs na imagem e passar o Tesseract em cada uma delas. 

Após isso, criei um quadro no Trello para começar a organizar as minhas tasks e sub-tasks e também coloquei post-its com pequenos fluxos na mesa.

A primeira task foi criar o dataset, preferencialmente de uma forma que eu consiga gerar mais amostras caso necessário. Achei algumas amostras no Google Images e no Bing, mas não em boa quantidade, então decidi pegar um modelo em branco de uma CNH e com o OpenCV preencher com dados fictícios e depois adicionar um pouco de ruído e variar um pouco a posição em que os textos eram colocados.

Com o dataset pronto,  a próxima task foi tentar utilizar o Tesseract na imagem toda, sem muitos tratamentos, para poder ter uma base a qual poderia usar como ponto de partida.

Com uma base pronta, eu parti para a tentativa de fazer por detecção de contornos e extraindo retângulos da imagem para poder passar uma imagem mais clara para o Tesseract, e assim aumentar a chance de acerto e também para poder alcançar o requisito opcional de extrair outras informações. Não ficou perfeito, há muito espaço pra melhoria mas funciona consideravelmente bem.

Depois de conseguir um extrator razoável, fui para a parte final de organizar o código para ser executado como script e criando um notebook no Google Colab para montar um ambiente sem precisar baixar localmente.
