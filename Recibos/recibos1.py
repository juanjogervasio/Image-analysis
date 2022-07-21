#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:12:30 2021

@author: mint
"""

from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
import pytesseract
import os
import time
#import numpy as np

t0 = time.time()
#Inicializo el Tesseract OCR
#En Linux:
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

"""
#En Windows:
pytesseract.pytesseract.tesseract_cmd = 
"""

# Convierto los pdf en imagen.
#1ro: genero una "lista" con el contenido del pdf
archivo = input("Ingresar nombre del archivo: ")
path = r"/home/mint/Desktop/Analisis\ de\ Recibos/Recibos/" + archivo

#Aca voy a guardar la informacion:
info=[]

#Aca voy a guardar los errores (paginas donde no esta el codigo buscado):
vacios=[]

#Inicializo contadores.
p=-1
k=0
i=1

while p:
    #Abro el pdf de a 20 paginas
    PDF = convert_from_path(path, first_page= p+1, last_page= k+20)

    #2do: convierto cada pagina del pdf en imagen
    for pagina in PDF:
        pagina.save("imagen"+str(i)+".jpg", "JPEG")
        
        #Abro la imagen correspondiente a la pagina i-esima:
        imagen = Image.open(r'/home/mint/Desktop/Analisis\ de\ Recibos/Recibos/imagen'+str(i)+'.jpg')
        
        #Recorto en la seccion de la fecha
        box = (32,354 , 250, 400)
        cropped = imagen.crop(box)
        contraste = ImageEnhance.Contrast(cropped).enhance(2)
        
        #Extraigo el contenido de la imagen
        fecha = pytesseract.image_to_string(contraste)
        
        #Recorto en la seccion del nombre
        box = (610,150 , 880, 185)
        cropped = imagen.crop(box)
        contraste = ImageEnhance.Contrast(cropped).enhance(2)
        
        #Extraigo el contenido de la imagen
        nombre = pytesseract.image_to_string(contraste)
        
        #Recorto en la seccion de los datos
        box = (32,320 , 1120, 945)
        cropped = imagen.crop(box)
        contraste = ImageEnhance.Contrast(cropped).enhance(2)
        
        #Extraigo el contenido de la imagen
        text = pytesseract.image_to_string(contraste)
        
        #Busco en el texto los codigos que me interesan y guardo la informacion en
        #la lista 'info'.
        Lista = ["0300", "2760", "2762", "2554", "2555", "2665", "2680"]
        for codigo in Lista:
            if codigo in text:
                suma=0
                inicio=0
                while inicio >= 0:
                    inicio = text[suma:].find(codigo)          #Ubico el inicio de la linea
                    fin = text[suma + inicio:].find("\n")      #Ubico el fin de la linea
                    if inicio<0:
                        break
                    info.append("Pagina "+str(i).zfill(3)+" "+ nombre[:nombre.find("\n")] +" "+
                                fecha[:fecha.find("\n")]+" "+ text[suma+inicio:suma+inicio+fin])
                    suma += inicio+1
                    
            else:
                print("No se encontro el codigo ", codigo, " en la pagina ", i, "\n")
                vacios.append("No se encontro el codigo "+str(codigo)+" en la pagina "+str(i))
        
        imagen.close()
        ubicacion = os.path.join(r"/home/mint/Desktop/Analisis\ de\ Recibos/Recibos",
                                 "imagen"+str(i)+".jpg")
        os.remove(ubicacion)
        i += 1
    
    p=k+20
    k=p
    
    #Detengo el loop al llegar al final del archivo
    if len(PDF)!= 20:
        break



salida = open("Lectura " + archivo[:len(archivo)-4] + ".txt", "a")
#print("Lectura del archivo ", archivo, "\n")
print("Lectura del archivo ", archivo, "\n", file = salida)
for j in range(len(info)):
#    print(info[j])
    print(info[j], file = salida)

t1 = time.time()
tiempo = t1 - t0
print("\n", "Tiempo de ejecucion: ", int(tiempo//60), " minutos ", '{:.2f}'.format(tiempo%60),
      " segundos.", file=salida)

salida.close()

