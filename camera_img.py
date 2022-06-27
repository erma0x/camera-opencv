import numpy as np
import cv2 as cv
import sys
from time import sleep
import argparse
import cv2
from traitlets import Float
import os

# $python3 camera_img.py --porta_usb 0 --nome_cartella "visibile" --intervallo_secondi 2

parser = argparse.ArgumentParser(description='Test fotografie ad intervalli regolari con tutti i tipi di videocamere disponibili per OpenCV')

parser.add_argument('--porta_usb', type = int, required=True , default=1, help="numero porta usb del dispositivo")                      # ID PORTA USB DISPOSITIVO
parser.add_argument('--nome_cartella', type = str, required=True, default="viz", help="nome cartella esistente dentro img/ dove salvare le foto")                 # nome cartella img in cui salvare le foto
parser.add_argument('--intervallo_secondi', type = float,default = 4.0 , help="intervallo di secondi fra 2 fotografie")     

args = parser.parse_args()


images_folders = sys.path[0]+"/"+"img"

if not os.path.exists(images_folders):
    os.makedirs(images_folders)
    
newpath = images_folders+"/"+ args.nome_cartella 

if not os.path.exists(newpath):
    os.makedirs(newpath)
    
    


# Inserisci 1 e connetti la videocamera al computer tramite USB
# se non funziona prova tutte le porte USB lanciando questo script.
# KEY_USB = 0
KEY_USB = args.porta_usb
CARTELLA = args.nome_cartella
INTERVALLO_SECONDI = args.intervallo_secondi



def rescale_frame(frame, percent=75):
    '''
    riscala l'immagine della videocamera in base ad una percentuale. 
    percent = 100 ,  1 : 1    non cambi la dimensione.
    percent = 150 ,  1 : 1.5  scali di una volta e mezzo
    percent = 50  ,  1 : 0.5  scali di mezza volta
    '''
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)


# inizializza l'oggetto videocamera
cap = cv.VideoCapture(KEY_USB)
sleep(0.1)

# contatore salva foto
i = 0

while True:
    #cattura frame per frame dalla videocamera
    ret, frame = cap.read()
    # se ret non è uguale a True, esci dall'loop
    if not ret:
        print("impossible ricevere immagini dalla videocamera")
        sleep(2)

   # frame_modified = rescale_frame(frame, percent=30)

    if np.array(frame).any(): 
        i+=1
        path_immagine = sys.path[0]+"/img/"+CARTELLA+"/foto_"+str(i)+".png"
        cv2.imwrite(path_immagine,frame) 
        sleep(2)
        img = cv2.imread(path_immagine)

         # frame_modified = rescale_frame(img, percent=30)
        
        cv.imshow('immagine videocamera', img )

        sleep(INTERVALLO_SECONDI)
