# Importando as Bibliotecas
from PIL import ImageFont, ImageDraw, Image
from cv2 import threshold
from easyocr import Reader
import numpy as np
import cv2
 
lista_idiomas = "pt"
idiomas = lista_idiomas.split(",")
fonte = 'Keyboard.ttf'
camera = cv2.VideoCapture(0)
 
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
 
if camera.isOpened():
   while True:
       conectado, frame = camera.read()
 
       if not conectado:
           break
       else:
           cv2.imshow("Vídeo da Webcam", frame)
          
           key = cv2.waitKey(32)
 
           if key == 27:
               camera.release()
               cv2.destroyAllWindows()
               break
 
           if key == 32:
               reader = Reader(idiomas)
               resultados = reader.readtext(frame)
               for(caixa, texto, prob) in resultados:
                       if prob >= 0.6:
                               te, td, bd, be = coord_caixa(caixa)
                               frame = desenha_caixa(frame, te, bd)
                               frame = fundo_texto(texto, te[0], te[1], frame, fonte, tam_fonte, cor_fundo)
                               frame = escreve_texto(texto, te[0], te[1], frame, fonte, cor_fonte, tam_fonte)
               cv2.imwrite("images/teste.jpeg", frame)