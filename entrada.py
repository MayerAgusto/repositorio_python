import cv2
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# ------funciones para las interfaces
def inicializar_frame(size_x, size_y):
    frame_t = LabelFrame(tab1, bg="white", width=size_x, height=size_y)
    return frame_t


def inicializar_label(frame_t, size_x, size_y):
    label_t = Label(frame_t, bg="white", width=size_x, height=size_y)
    return label_t


def show_tiny_frame(frame_t, int_x, int_y):
    frame_t = cv2.resize(frame_t, (int_x, int_y))
    frame_t = cv2.cvtColor(frame_t, cv2.COLOR_BGR2RGB)
    frame_t = ImageTk.PhotoImage(Image.fromarray(frame_t))
    return frame_t


# valores de entrada
lista = ['E:/5sos.mp4', 'D:/temp/MOV_0700.mp4', 'E:/5sos.mp4']
# creacion de los objetos cap
global cap
global cap_1
global cap_2

def iniciar(a,b,c):
    cap = cv2.VideoCapture(a)
    cap_1 = cv2.VideoCapture(b)
    cap_2 = cv2.VideoCapture(c)
    return cap,cap_1,cap_2

cap,cap_1,cap_2 = iniciar(lista[0],lista[1],lista[2])
lista_capturas = [cap,cap_1,cap_2]

# --------------- iniciar la creacion de interfaz
window = Tk()
window.title("Camaras")
window.geometry('1200x620')
window.resizable(0, 0)

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Camaras piso 1')

lbl1 = Label(tab1, text='label1')
lbl1.pack()

ventana01 = inicializar_frame(400, 280)
ventana01.place(x=0, y=0)
L1 = inicializar_label(ventana01, 400, 280)
L1.pack()

ventana02 = inicializar_frame(400, 280)
ventana02.place(x=0, y=280)
L2 = inicializar_label(ventana02, 400, 280)
L2.pack()

ventana03 = inicializar_frame(800, 560)
ventana03.place(x=410, y=0)
L3 = inicializar_label(ventana03, 800, 560)
L3.pack()
# ---------------funciones de acciones
def callback(event):
    aux = lista[0]
    lista[0] = lista[2]
    lista[2] = aux
    lista_capturas[0] = cv2.VideoCapture(lista[0])
    lista_capturas[2] = cv2.VideoCapture(lista[2])
    print('clicked', lista[0], lista[2], 'cap hecho')

def callback1(event):
    aux = lista[1]
    lista[1] = lista[2]
    lista[2] = aux
    lista_capturas[1] = cv2.VideoCapture(lista[1])
    lista_capturas[2] = cv2.VideoCapture(lista[2])
    print('clicked', lista[1], lista[2], 'cap hecho')
# ----------------fin de funciones de acciones
L1.bind("<Button-1>", callback)
L2.bind("<Button-1>", callback1)

tab_control.pack(expand=1, fill='both')
# ----------------------- fin de interfaces


if (lista_capturas[0].isOpened() == False or lista_capturas[1].isOpened() == False or lista_capturas[2].isOpened() == False):
    print('Vide no pudo ser capturado')

while (True):
    if lista_capturas[0].isOpened() != False:
        ret, frame = lista_capturas[0].read()
        if (ret == True):
            frame = show_tiny_frame(frame, 400, 280)
            L1['image'] = frame

    if lista_capturas[1].isOpened() != False:
        ret_1, frame_1 = lista_capturas[1].read()
        if (ret_1 == True):
            frame_1 = show_tiny_frame(frame_1, 400, 280)
            L2['image'] = frame_1

    if lista_capturas[2].isOpened() != False:
        ret_2, frame_2 = lista_capturas[2].read()
        if (ret_2 == True):
            frame_2 = show_tiny_frame(frame_2, 800, 560)
            L3['image'] = frame_2

    if (lista_capturas[0].isOpened() == False or lista_capturas[1].isOpened() == False or lista_capturas[2].isOpened() == False):
        print('Vide no pudo ser capturado')

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    window.update()

#cap.release()
#cv2.destroyWindow()
