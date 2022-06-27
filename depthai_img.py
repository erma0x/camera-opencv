import sys
import argparse
from datetime import datetime
from time import sleep
import cv2
import depthai as dai
import numpy as np
import os
# esempio di come lanciare lo script                      
# python3  .\tests\camera\depthai_test.py --id_camera "14442C1001293DD700" --nome_cartella "viz" --intervallo_secondi 4


# parametri camera depthaAI
nome_pannello_di_controllo = "video"
FPS_frame = 7                                  # fps frame per second : intervallo fra 1-120 
manual_focus_parameter = 200                    # focus manuale : intervallo fra 0-255 
expTime = 2000                                 # tempo di esposizione in milliseconds : intervallo fra 1-100_000
sensIso = 230                                   # sensibilità del sensore della fotocamera : intervallo fra 0-500
video_size_x = 1920*2                             # grandezza video asse X in pixels
video_size_y = 1080*2                              # grandezza video asse Y in pixels
                          


parser = argparse.ArgumentParser(description='Test fotografie ad intervalli regolari con camere di tipo OAK')

parser.add_argument('--id_camera', type=str, required=True , default="14442C1001293DD700" ,help="ID della camera OAK")     # ID modello videocamera OAK passato da linea di comando
parser.add_argument('--nome_cartella', type=str, required=True, default="viz", help="nome cartella esistente dentro img/ dove salvare le foto")            # nome cartella img in cui salvare le foto
parser.add_argument('--intervallo_secondi', type=float ,default=4.0 ,help="intervallo di secondi fra 2 fotografie")     

args = parser.parse_args()


images_folders = sys.path[0]+"/"+"img"

if not os.path.exists(images_folders):
    os.makedirs(images_folders)
    
newpath = sys.path[0]+"/"+images_folders+"/"+ args.nome_cartella 

if not os.path.exists(newpath):
    os.makedirs(newpath)
    

def disegna_difetti(img):
    '''
    disegna linee in maniera automatica sull'immagine
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 90, 120)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength=5, maxLineGap=20)
    if np.array(lines).any():
        for line in lines: # Draw lines on the image
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 3)
    return img




ID_CAMERA = args.id_camera
NOME_CARTELLA = args.nome_cartella
INTERVALLO_SECONDI = args.intervallo_secondi


# inizializza la videocamera con depthai
pipeline = dai.Pipeline()
controllo = dai.CameraControl()
camRgb = pipeline.createColorCamera()

xoutVideo = pipeline.createXLinkOut()
controlIn = pipeline.createXLinkIn()

xoutVideo.setStreamName(nome_pannello_di_controllo)
controlIn.setStreamName('control')

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)

# setta la risoluzione della vidocamera 
# modalità disponibili sono: 4k, 1080p, 12mega pixel (THE_4_K,THE_1080_P, THE_12_MP )
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)        # 4K

# setta i frame per secondo
camRgb.setFps(float(FPS_frame))


# modalita' focus automatico: AUTO, MACRO, CONTINUOUS_VIDEO, CONTINUOUS_PICTURE, OFF, EDOF
controllo.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
#controllo.setManualFocus(manual_focus_parameter)


# setta la regione da zoommare e gestire con l'autofocus
#controllo.setAutoFocusRegion(dai.CameraControl,int(1670),int(770),int(660),int(500))


# setta la grandezza video con le coordinate X & Y in pixels
camRgb.setVideoSize(video_size_x, video_size_y)


# modalità disponibili: ACTION, STEADYPHOTO
controllo.setSceneMode(dai.CameraControl.SceneMode.ACTION)


# setta il tempo di esposizione manuale
controllo.setManualExposure(expTime,sensIso)
#controlQueue.send(controllo)

xoutVideo.input.setBlocking(False)

xoutVideo.input.setQueueSize(1)

camRgb.video.link(xoutVideo.input)

found, device_info = dai.Device.getDeviceByMxId(ID_CAMERA)

if not found:
    raise RuntimeError("Videocamera non trovata! Perfavore riprova")

i=0

#try:
with dai.Device(pipeline, device_info) as device:
    
    video = device.getOutputQueue( name = nome_pannello_di_controllo, maxSize = 1, blocking = False)
    
    controlQueue = device.getInputQueue('control')

    ctrl = dai.CameraControl()

    ctrl.setManualExposure(expTime, sensIso)
    ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.CONTINUOUS_PICTURE)

    controlQueue.send(ctrl)

    cv2.namedWindow(nome_pannello_di_controllo, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(nome_pannello_di_controllo, video_size_x, video_size_y)
    
    while True:
        videoIn = video.get()

        frame =  videoIn.getCvFrame()

        #risultato_finale = disegna_difetti( img = frame  )

        cv2.imshow(nome_pannello_di_controllo, frame)
        
        i+=1
        
        sleep(float(INTERVALLO_SECONDI))
        
        cv2.imwrite(sys.path[0]+"/img/"+str(NOME_CARTELLA)+"/foto_"+str(i)+".png",frame) 

        if cv2.waitKey(2) == ord('c'):
            break

#except RuntimeError:
  #  print("Errore nel catturare le fotografie")
