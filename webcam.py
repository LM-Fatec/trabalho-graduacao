# Importando as Bibliotecas
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from matplotlib import pyplot as plt
from gtts import gTTS
import easyocr
import cv2
from playsound import playsound
import pyodbc
from datetime import datetime

server = "localhost,1433"
database = "FatecDB"
username = "sa"
password = "pwt945jau6"

# conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;UID='+username+';PWD='+ password)
# cursor = conn.cursor()

fonte = 'Arial.ttf'
 
cor_fonte = (0,0,0)
cor_fundo = (200,255,0)
cor_caixa = (200,255,0)
tam_fonte = 20
 
def coord_caixa(caixa):
       (te, td, bd, be) = caixa
       te = (int(te[0]), int(te[1]))
       td = (int(td[0]), int(td[1]))
       bd = (int(bd[0]), int(bd[1]))
       be = (int(be[0]), int(be[1]))
       return te, td, bd, be
 
def desenha_caixa(img, te,bd, cor_caixa=(200,255,0), espessura=2):
       cv2.rectangle(img, te, bd, cor_caixa, espessura)
       return img
 
def escreve_texto(texto, x, y, img, fonte, cor=(50, 50, 255), tamanho=22):
       fonte = ImageFont.truetype(fonte, tamanho)
       img_pil = Image.fromarray(img) 
       draw = ImageDraw.Draw(img_pil)
       draw.text((x, y-tamanho), texto, font = fonte, fill = cor)
       img = np.array(img_pil)
       return img
 
def fundo_texto(texto, x, y, img, fonte, tamanho=32, cor_fundo=(200, 255, 0)):
       fundo = np.full((img.shape), (0,0,0), dtype=np.uint8)
       texto_fundo = escreve_texto(texto, x, y, fundo, fonte, (255,255,255), tamanho=tamanho)
       texto_fundo = cv2.dilate(texto_fundo,(np.ones((3,5),np.uint8)))
       fx,fy,fw,fh = cv2.boundingRect(texto_fundo[:,:,2])
       cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), cor_fundo, -1)
       return img


# 0 Utiliza a camera do notebook, 1 Utiliza a camera do celular
video = cv2.VideoCapture(1)

while True:
    check, frame = video.read()
    
    # Redimensiona o tamanho do frame para um tamanho padrão
    frame = cv2.resize(frame, (640, 480))
    
    # Utiliza a biblioteca EasyOCR para identificar os textos no frame
    reader = easyocr.Reader(['pt'], gpu=False)
    imagem_cp = frame.copy()
    result = reader.readtext(frame)

    agora = datetime.now()
    data = agora.strftime("%H:%M:%S")

    # Salva o frame original
    cv2.imwrite("images/original/captura-" + data +".jpeg", frame)
    alergenicos = ["CONTÉM GLUTÉN", "NÃO CONTÉM GLÚTEN"]
    alergenicos = [each_string.lower() for each_string in alergenicos]
    for(caixa, texto, prob) in result:
        probabilidade = 0.5 # Número de referência para confiança
        if prob >= probabilidade:

            # Realiza o quadro em volta do texto identificado
            te, td, bd, be = coord_caixa(caixa)
            textoFormatado = f'{texto} - {str(round(prob, 2) * 100)}%'
            if any(texto.lower() in ele for ele in alergenicos):
                frame = desenha_caixa(frame, te, bd)
                frame = fundo_texto(textoFormatado, te[0], te[1], frame, fonte, tam_fonte, cor_fundo)
                frame = escreve_texto(textoFormatado, te[0], te[1], frame, fonte, cor_fonte, tam_fonte)        

                # Salva a imagem capturada
                cv2.imwrite("images/captura-" + data + ".jpeg", frame)

                # Utiliza do Google Translate para ditar oque foi encontrado na imagem
                tts = gTTS(texto, lang='pt', tld='com.br')
                tts.save("sounds/sound-" + data + ".mp3")
                playsound("sounds/sound-" + data + ".mp3")
    cv2.imshow("OCR", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       video.release()
       cv2.destroyAllWindows()
       break