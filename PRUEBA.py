# Packages
import numpy as np
import cv2 as cv
import cv2 as cv2
import numpy as np
import datetime
from threading import Thread,Semaphore
"""import pymongo"""
"""from bson.objectid import ObjectId"""
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# My Classes
import MyPerson
import MyFrameFeatures

# Inicializacion de semaforo
semaforo = Semaphore(1)

#################
# BASE DE DATOS #
#################
"""
Mongo_baseDatos = "ForoPrueba"
Mongo_coleccion = "prueba"
cliente = pymongo.MongoClient("mongodb+srv://Cesar:1234@cluster0.ihcp8.mongodb.net/Foro?retryWrites=true&w=majority")
baseDatos =cliente[Mongo_baseDatos]
coleccion = baseDatos[Mongo_coleccion]
ID_doc = "5f931b16879144ec11b4446a"
idBuscar = {"_id":ObjectId(ID_doc)}
documento = coleccion.find(idBuscar)
"""

"""
def añadir():
    hilo = Thread(target=add)
    hilo.start()

def restar():
    hilo = Thread(target=subtract)
    hilo.start()
    
def add():
    global semaforo
    semaforo.acquire()
    valor=documento[0]["Cantidad"]+1
    coleccion.update_one({"_id":ObjectId(ID_doc)}, {"$set": {"Cantidad": valor }})

    semaforo.release()

def subtract():
    global semaforo
    semaforo.acquire()
    valor=documento[0]["Cantidad"]-1
    coleccion.update_one({"_id":ObjectId(ID_doc)}, {"$set": {"Cantidad": valor }})

    semaforo.release()
"""

###############################
 

# Implementando funcion principal
def detection(cap, nameCAM, frFts):
    global aforo_total, persons, pid
    ret, frame = cap.read()

    for i in persons:
        i.age_one()

    frame = cv.resize(frame, (640,480)) # Cambiar el tamaño de cada cuadro (fotograma) ancho y alto, resize every frame, width and height
    #print(frame.shape) # row (height), column (width) and channels (if the image is color)

    datet = str(datetime.datetime.now())
    cv.putText(frame, datet[0:21], (430, 470), font, .5, (0,0,0), 1, cv.LINE_AA)
    
    #########################
    #   PRE-PROCESAMIENTO   #
    #########################
    
    # Aplica sustraccion de fondo (Apply background subtraction)
    fgmask = fgbg.apply(frame)

    # Binarizacion para eliminar sombras (color gris), Binarization to eliminate shadows (gray color)
    ret , imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
    mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, frFts.kernelOp()) # Quitar ruido (Remove noise)
    mask = cv.morphologyEx(mask , cv.MORPH_CLOSE, frFts.kernelCl()) # Juntar las regiones blancas (join white regions)
    

    #################
    #   CONTORNOS   #
    #################
    
    # hierarchy = return (next contour in same hierarchy, previous contour in same hierarchy, child, parent)
    # contours = return edge matrix (just the parent contour, child contour is left behind)
    contours, hierarchy = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv.contourArea(cnt)

        if area > frFts.area_Minimum_Human():
            print(nameCAM,'Area Detectada: ',area, ', Area minima de humano: ', frFts.area_Minimum_Human())

            #################
            #   TRACKING    #
            #################

            # Caracteristicas del objeto como centro de masa o area (Features of the object as center of mass or area)
            M = cv.moments(cnt)
            # (cx, cy) is the Centroid (the arithmetic mean position)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            (x, y, w, h) = cv.boundingRect(cnt) # (x , y) = coordinates, (w, h) = width and height
            cv.circle(frame,(x,y), 12, (255,0,255), -1)

            new = True

            if cy in range(frFts.up_limit(), frFts.down_limit()): 

                for i in persons:
                    # Si el objeto no esta cerca de uno que ya se detecto antes
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                        
                        new = False
                        i.updateCoords(cx,cy) # Actualiza coordenadas en el objeto and resets age

                        if i.going_UP(frFts.line_down(),frFts.line_up()) == True:
                            semaforo.acquire()
                            aforo_total += 1
                            #añadir()
                            semaforo.release()
                            print(nameCAM,'AFORO TOTAL:', aforo_total)
                                
                        elif i.going_DOWN(frFts.line_down(),frFts.line_up()) == True:
                            semaforo.acquire()
                            aforo_total -= 1
                            #restar()
                            semaforo.release()
                            print(nameCAM, 'AFORO TOTAL:', aforo_total)
                        break
                    
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > frFts.down_limit():
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < frFts.up_limit():
                            i.setDone()

                    if i.timedOut():
                        # Sacar i de la lista persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i # Liberar memoria (Release memory
                    
                if new == True:
                    p = MyPerson.Person(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1

            #################
            #   DIBUJOS     #
            #################

            cv.circle(frame,(cx,cy), 6, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv.drawContours(frame, cnt, -1, (0,255,0), 3)
            
    #END for cnt in contours
            
    #########################
    # DIBUJAR TRAYECTORIAS  #
    #########################

    for i in persons:
        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
    
    #################
    #      Lines    #
    #################

    cv.putText(frame, 'Aforo Total: '+str(aforo_total), (50, 50), font, 1, (0,185,255), 2, cv.LINE_AA)
    frame = cv.polylines(frame,[frFts.coord_redl()],False,(0,0,255),thickness=2)
    frame = cv.polylines(frame,[frFts.coord_bluel()],False,(255,0,0),thickness=2)
    frame = cv.polylines(frame,[frFts.coord_fwl()],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame,[frFts.coord_lwl()],False,(255,255,255),thickness=1)

    #################
    #   FOTOGRAMAS  #
    #################

    #cv.imshow(nameCAM, frame)
    #cv.imshow('Mask', mask)
    return frame
#END 

def detection2(cap, nameCAM, frFts):
    global aforo_total, persons2, pid2
    ret, frame = cap.read()

    for i in persons2:
        i.age_one()

    frame = cv.resize(frame, (640,480)) # Cambiar el tamaño de cada cuadro (fotograma) ancho y alto, resize every frame, width and height
    #print(frame.shape) # row (height), column (width) and channels (if the image is color)

    datet = str(datetime.datetime.now())
    cv.putText(frame, datet[0:21], (430, 470), font, .5, (0,0,0), 1, cv.LINE_AA)
    
    #########################
    #   PRE-PROCESAMIENTO   #
    #########################
    
    # Aplica sustraccion de fondo (Apply background subtraction)
    fgmask = fgbg.apply(frame)
    
    # Binarizacion para eliminar sombras (color gris), Binarization to eliminate shadows (gray color)
    ret , imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
    mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, frFts.kernelOp()) # Quitar ruido (Remove noise)
    mask = cv.morphologyEx(mask , cv.MORPH_CLOSE, frFts.kernelCl()) # Juntar las regiones blancas (join white regions)
    

    #################
    #   CONTORNOS   #
    #################
    
    # hierarchy = return (next contour in same hierarchy, previous contour in same hierarchy, child, parent)
    # contours = return edge matrix (just the parent contour, child contour is left behind)
    contours, hierarchy = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv.contourArea(cnt)

        if area > frFts.area_Minimum_Human():
            print(nameCAM,'Area Detectada: ',area, ', Area minima de humano: ', frFts.area_Minimum_Human())

            #################
            #   TRACKING    #
            #################

            # Caracteristicas del objeto como centro de masa o area (Features of the object as center of mass or area)
            M = cv.moments(cnt)
            # (cx, cy) is the Centroid (the arithmetic mean position)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            (x, y, w, h) = cv.boundingRect(cnt) # (x , y) = coordinates, (w, h) = width and height
            cv.circle(frame,(x,y), 12, (255,0,255), -1)

            new = True

            if cy in range(frFts.up_limit(), frFts.down_limit()): 

                for i in persons2:
                    # Si el objeto no esta cerca de uno que ya se detecto antes
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                        
                        new = False
                        i.updateCoords(cx,cy) # Actualiza coordenadas en el objeto and resets age

                        if i.going_UP(frFts.line_down(),frFts.line_up()) == True:
                            semaforo.acquire()
                            aforo_total += 1
                            #añadir()
                            semaforo.release()
                            print(nameCAM,'AFORO TOTAL:', aforo_total)
                                
                        elif i.going_DOWN(frFts.line_down(),frFts.line_up()) == True:
                            semaforo.acquire()
                            aforo_total -= 1
                            #restar()
                            semaforo.release()
                            print(nameCAM, 'AFORO TOTAL:', aforo_total)
                        break
                    
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > frFts.down_limit():
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < frFts.up_limit():
                            i.setDone()

                    if i.timedOut():
                        # Sacar i de la lista persons
                        index = persons2.index(i)
                        persons2.pop(index)
                        del i # Liberar memoria (Release memory
                    
                if new == True:
                    p = MyPerson.Person(pid2, cx, cy, max_p_age)
                    persons2.append(p)
                    pid2 += 1

            #################
            #   DIBUJOS     #
            #################

            cv.circle(frame,(cx,cy), 6, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv.drawContours(frame, cnt, -1, (0,255,0), 3)
            
    #END for cnt in contours
            
    #########################
    # DIBUJAR TRAYECTORIAS  #
    #########################

    for i in persons2:
        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
    
    #################
    #      Lines    #
    #################

    cv.putText(frame, 'Aforo Total: '+str(aforo_total), (50, 50), font, 1, (0,185,255), 2, cv.LINE_AA)
    frame = cv.polylines(frame,[frFts.coord_redl()],False,(0,0,255),thickness=2)
    frame = cv.polylines(frame,[frFts.coord_bluel()],False,(255,0,0),thickness=2)
    frame = cv.polylines(frame,[frFts.coord_fwl()],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame,[frFts.coord_lwl()],False,(255,255,255),thickness=1)

    #################
    #   FOTOGRAMAS  #
    #################

    cv.imshow(nameCAM, frame)
    #cv.imshow('Mask', mask)

#END 

# System Begin

if __name__ == '__main__':

    # Contadores de entrada y salida (In and out counters)
    aforo_total = 20

    # Capturar video (Video Capture)
    cap = cv.VideoCapture(2)
    #cap2 = cv.VideoCapture(2)

    # Object for a frame and video features
    frFtrs = MyFrameFeatures.Frame_Features(cap)
    
    # Sustractor de fondo (Background sustractor)
    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True) # Mixture of Gaussian (MOG)

    # Variables
    font = cv.FONT_HERSHEY_SIMPLEX
    persons = []
    persons2 = []
    max_p_age = 5
    pid = 1 # Identificacion de persona (Person ID)    
    pid2 = 1 # Identificacion de persona (Person ID)   


'''Direcciones donde se extraera el video  4 camaras'''
import cv2
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
'''Direcciones donde se extraera el video  4 camaras'''
lista_camaras = ['https://192.168.0.104:8080/video','*','*','*']
cap = None
cap2 = None
cap3= None
cap4 = None

'''recibe la direccion y establece la conexion '''
def video_capture(a):
    cap = cv2.VideoCapture(a)
    return cap
''' inicializa las variables donde capturamos el video en caso de no encontrar no inicializa  '''
if lista_camaras[0] !='*':
    cap = video_capture(lista_camaras[0])
if lista_camaras[1] !='*':
    cap2 = video_capture(lista_camaras[1])
if lista_camaras[2] != '*':
    cap3 = video_capture(lista_camaras[2])
if lista_camaras[3] != '*':
    cap4 = video_capture(lista_camaras[3])

'''creacion de ventana principal'''
window = Tk()
window.title("Camaras")
window.geometry('1200x620')
window.resizable(0, 0)

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Camaras piso 1')

lbl1 = Label(tab1, text='label1')
lbl1.pack()
frame01 = LabelFrame(tab1, bg="red", width=320, height=200)
frame01.place(x=0, y=0)
L1 = Label(frame01,bg="red", width=320, height=200)
L1.pack()

frame02 = LabelFrame(tab1, bg="blue", width=320, height=200)
frame02.place(x=0, y=200)
L2 = Label(frame02,bg="blue", width=320, height=200)
L2.pack()

frame03 = LabelFrame(tab1, bg="white", width=320, height=200)
frame03.place(x=0, y=400)
L3 = Label(frame03, bg="white", width=320, height=200)
L3.pack()

frame04 = LabelFrame(tab1, bg="orange", width=900, height=600)
frame04.place(x=320, y=0)
L4 = Label(frame04,width=900, height=600)
L4.pack()

'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''
def callback(event):
    frame04.focus_set()
    aux = lista_camaras[0]
    lista_camaras[0] = lista_camaras[3]
    lista_camaras[3] = aux
    if lista_camaras[0] !='*':
        cap =video_capture(lista_camaras[0])
    if lista_camaras[3] !='*':
        cap4 =video_capture(lista_camaras[3])
    print('clicked',lista_camaras[0],lista_camaras[3] ,'cap hecho')

'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''
def callback1(event):
    frame04.focus_set()
    aux = lista_camaras[1]
    lista_camaras[1] = lista_camaras[3]
    lista_camaras[3] = aux
    if lista_camaras[1] !='*':
        cap2 =video_capture(lista_camaras[1])
    if lista_camaras[3] !='*':
        cap4 =video_capture(lista_camaras[3])
    print('clicked',lista_camaras[1],lista_camaras[3] ,'cap hecho')

'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''
def callback2(event):
    frame04.focus_set()
    aux = lista_camaras[2]
    lista_camaras[2] = lista_camaras[3]
    lista_camaras[3] = aux
    if lista_camaras[2] !='*':
        cap3 =video_capture(lista_camaras[2])
    if lista_camaras[3] !='*':
        cap4 =video_capture(lista_camaras[3])
    print('clicked',lista_camaras[2],lista_camaras[3] ,'cap hecho')

'''Se le asigna cada accion a cada frame'''
L1.bind("<Button-1>", callback)
L2.bind("<Button-1>", callback1)
L3.bind("<Button-1>", callback2)

tab_control.pack(expand=1, fill='both')


'''recibe la direccion y establece la conexion '''




while(cap.isOpened()):
    if lista_camaras[0] != '*':
        cap = video_capture(lista_camaras[0])
        img = detection(cap, "frame1", frFtrs)
        img = cv2.resize(img, (320, 200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img))
        L1['image'] = img
    if lista_camaras[1] != '*':
        cap2 = video_capture(lista_camaras[1])
        img2 = cap2.read()[1]
        img2 = cv2.resize(img2, (320, 200))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img2 = ImageTk.PhotoImage(Image.fromarray(img2))
        L2['image'] = img2
    if lista_camaras[2] != '*':
        cap3 = video_capture(lista_camaras[2])
        img3 = cap3.read()[1]
        img3 = cv2.resize(img3, (320, 200))
        img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
        img3 = ImageTk.PhotoImage(Image.fromarray(img3))
        L3['image'] = img3
    if lista_camaras[3] != '*':
        cap4 = video_capture(lista_camaras[3])
        img4 = cap4.read()[1]
        img4 = cv2.resize(img4, (900, 600))
        img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
        img4 = ImageTk.PhotoImage(Image.fromarray(img4))
        L4['image'] = img4

    if cv.waitKey(25) == ord('q'): # Terminar la ejecución
        print("AFORO TOTAL:", aforo_total)
        break

        
    #################
    #   LIMPIEZA    #
    #################

    cap.release()
    cv.destroyAllWindows()