import cv2
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

'''clase camara'''


class Camara:
    def __init__(self, realpart):
        self.idcam = realpart
        self.cam = None


c1 = Camara(1)
c2 = Camara(1)
c3 = Camara(1)
c4 = Camara(-1)
CamList = [c1, c2, c3, c4]
'''Direcciones donde se extraera el video  4 camaras'''
lista_camaras = [2, 1, 3, -1]

cap = None
cap2 = None
cap3 = None
cap4 = None

'''recibe la direccion y establece la conexion '''


def video_capture(a):
    cap = cv2.VideoCapture(a)
    return cap


''' inicializa las variables donde capturamos el video en caso de no encontrar no inicializa  '''
if lista_camaras[0] != -1:
    cap = video_capture(lista_camaras[0])
if lista_camaras[1] != -1:
    cap2 = video_capture(lista_camaras[1])
if lista_camaras[2] != -1:
    cap3 = video_capture(lista_camaras[2])
if lista_camaras[3] != -1:
    cap4 = video_capture(lista_camaras[3])

for x in CamList:
    if x.idcam != -1:
        x = video_capture(x.idcam)

'''creacion de ventana principal'''
window = Tk()
window.title("Camaras")
window.geometry('1200x630')
window.resizable(0, 0)

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Camaras piso 1')

lbl1 = Label(tab1, text='label1')
lbl1.pack()
frame01 = LabelFrame(tab1, bg="red", width=320, height=200)
frame01.place(x=0, y=0)
L1 = Label(frame01, bg="red", width=320, height=200)
L1.pack()

frame02 = LabelFrame(tab1, bg="blue", width=320, height=200)
frame02.place(x=0, y=200)
L2 = Label(frame02, bg="blue", width=320, height=200)
L2.pack()

frame03 = LabelFrame(tab1, bg="white", width=320, height=200)
frame03.place(x=0, y=400)
L3 = Label(frame03, bg="white", width=320, height=200)
L3.pack()

frame04 = LabelFrame(tab1, bg="orange", width=900, height=600)
frame04.place(x=320, y=0)
L4 = Label(frame04, width=900, height=600)
L4.pack()

'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''


def callback(event):
    frame04.focus_set()
    # camara 0
    if lista_camaras[3] == -1:
        aux = lista_camaras[0]
        lista_camaras[0] = lista_camaras[3]
        lista_camaras[3] = aux
        cap = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[0])
    elif lista_camaras[1] == -1:
        aux = lista_camaras[1]
        lista_camaras[1] = lista_camaras[3]
        lista_camaras[3] = aux
        cap2 = video_capture(lista_camaras[1])
        cap = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[0])
    else:
        aux = lista_camaras[2]
        lista_camaras[2] = lista_camaras[3]
        lista_camaras[3] = aux
        cap3 = video_capture(lista_camaras[2])
        cap = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[0])

    '''if lista_camaras[3] == -1:

    else:
        temp = lista_camaras[3] 
        cout = 0
        for x in lista:
          if x == -1:
            #print(x)
          break
        cout =  cout + 1
        lista_camara[cout] = temp
        lista_camara[]'''

    print('clicked', lista_camaras[0], lista_camaras[3], 'cap hecho')


'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''


def callback1(event):
    frame04.focus_set()
    # camara 1
    if lista_camaras[3] == -1:
        aux = lista_camaras[1]
        lista_camaras[1] = lista_camaras[3]
        lista_camaras[3] = aux
        cap2 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[1])
    elif lista_camaras[0] == -1:
        aux = lista_camaras[0]
        lista_camaras[0] = lista_camaras[3]
        lista_camaras[3] = aux
        cap = video_capture(lista_camaras[0])
        cap2 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[1])
    else:
        aux = lista_camaras[2]
        lista_camaras[2] = lista_camaras[3]
        lista_camaras[3] = aux
        cap3 = video_capture(lista_camaras[2])
        cap2 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[1])
    print('clicked', lista_camaras[1], lista_camaras[3], 'cap hecho')


'''Evento de click en un frame, cambia la transmision del frame pequeño al frame principal '''


def callback2(event):
    frame04.focus_set()
    # camara 2
    if lista_camaras[3] == -1:
        aux = lista_camaras[2]
        lista_camaras[2] = lista_camaras[3]
        lista_camaras[3] = aux
        cap3 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[2])
    elif lista_camaras[0] == -1:
        aux = lista_camaras[0]
        lista_camaras[0] = lista_camaras[3]
        lista_camaras[3] = aux
        cap = video_capture(lista_camaras[0])
        cap3 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[2])
    else:
        aux = lista_camaras[1]
        lista_camaras[1] = lista_camaras[3]
        lista_camaras[3] = aux
        cap2 = video_capture(lista_camaras[1])
        cap3 = video_capture(lista_camaras[3])
        cap4 = video_capture(lista_camaras[2])

    print('clicked', lista_camaras[2], lista_camaras[3], 'cap hecho')


'''Se le asigna cada accion a cada frame'''
L1.bind("<Button-1>", callback)
L2.bind("<Button-1>", callback1)
L3.bind("<Button-1>", callback2)

tab_control.pack(expand=1, fill='both')

'''En el bucle permite capturar el video'''
''' cap.read() , captura el video'''
'''cv2.resize(img, (320, 200)) , cambia el tamaño del video a el tamaño establecido'''
'''img = ImageTk.PhotoImage(Image.fromarray(img)) ,  covierte el video a imagen'''
'''L1['image'] = img , ingresa la imagen al label seleccionado'''
''' este proceso se repite a las 4 camaras '''
while True:
    if lista_camaras[0] != -1:
        cap = video_capture(lista_camaras[0])
        img = cap.read()[1]
        img = cv2.resize(img, (320, 200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img))
        L1['image'] = img
    if lista_camaras[1] != -1:
        cap2 = video_capture(lista_camaras[1])
        img2 = cap2.read()[1]
        img2 = cv2.resize(img2, (320, 200))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img2 = ImageTk.PhotoImage(Image.fromarray(img2))
        L2['image'] = img2
    if lista_camaras[2] != -1:
        cap3 = video_capture(lista_camaras[2])
        img3 = cap3.read()[1]
        img3 = cv2.resize(img3, (320, 200))
        img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
        img3 = ImageTk.PhotoImage(Image.fromarray(img3))
        L3['image'] = img3
    if lista_camaras[3] != -1:
        cap4 = video_capture(lista_camaras[3])
        img4 = cap4.read()[1]
        img4 = cv2.resize(img4, (900, 600))
        img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
        img4 = ImageTk.PhotoImage(Image.fromarray(img4))
        L4['image'] = img4

    window.update()

