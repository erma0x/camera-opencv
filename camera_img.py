import sys
from time import sleep
import argparse
import os

import numpy as np
import cv2 as cv
# $python3 camera_img.py --porta_usb 0 --nome_cartella "visibile" --intervallo_secondi 2

parser = argparse.ArgumentParser(description='Test fotografie ad intervalli regolari con tutti i tipi di videocamere disponibili per OpenCV')

parser.add_argument('--porta_usb', type = int, required=False , default = 2 , help = "numero porta usb del dispositivo")                                # ID PORTA USB DISPOSITIVO
parser.add_argument('--nome_cartella', type = str, required=False, default = "viz", help="nome cartella esistente dentro img/ dove salvare le foto")  # nome cartella img in cui salvare le foto
parser.add_argument('--intervallo_secondi', type = float, default = 1.0 , help="intervallo di secondi fra due fotografie")     
parser.add_argument('--salva', type = float, default = True , help="salva le fotografie")     
parser.add_argument('--visualizza', type = float, default = True , help="visualizza o meno l'immagine in tempo reale")     
args = parser.parse_args()


images_folders = sys.path[0]+"/"+"img"

if not os.path.exists(images_folders):
    os.makedirs(images_folders)
    
newpath = images_folders+"/"+ args.nome_cartella 

if not os.path.exists(newpath):
    os.makedirs(newpath)
    
# Inserisci 1 e connetti la videocamera al computer tramite USB
# se non funziona prova tutte le porte USB lanciando questo script.
KEY_USB = args.porta_usb
CARTELLA = args.nome_cartella
INTERVALLO_SECONDI = args.intervallo_secondi

# inizializza l'oggetto videocamera
cap = cv.VideoCapture(KEY_USB)

# risoluzione 12.3 MegaPixels
cap.set(3, 4295)  # Set horizontal resolution
cap.set(4, 2864)  # Set vertical resolution

sleep(0.2)

i = 0 # contatore salva foto


while True:
    #cattura frame per frame dalla videocamera
    ret, frame = cap.read()

    # se ret non è uguale a True, esci dall'loop
    if not ret:
        print("impossible ricevere immagini dalla videocamera")
        sleep(2)

    if args.visualizza:
        cv.imshow('real time image',frame) 
        cv.waitKey(1)      # wait until user hits any key on keyboard

    if args.salva:
        if np.array(frame).any(): 
            i+=1
            path_immagine = sys.path[0]+"/img/"+CARTELLA+"/foto_"+str(i)+".png"
            
            cv.imwrite(path_immagine,frame) 
                       
            sleep(INTERVALLO_SECONDI)
