#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 22:22:05 2021

@author: mint
"""

from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
import pytesseract
import os
import numpy as np

#Inicializo el Tesseract OCR
#En Linux:
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
"""
#En Windows:
pytesseract.pytesseract.tesseract_cmd = 
"""

# Convierto los pdf en imagen.
#1ro: genero una "lista" con el contenido del pdf
archivo = input("Ingresar nombre de archivo: ")
path = r"/home/mint/Desktop/Analisis\ de\ Recibos/Recibos" + archivo
PDF = convert_from_path(path, 200)

#2do: convierto cada pagina del pdf en imagen
contador=0
for pagina in PDF:
    pagina.save("imagen"+str(contador)+".jpg", "JPEG")
    contador += 1

#Voy a buscar en cada imagen el texto que me interesa y despues borro todo

#Guardo todo lo que encuentre en una lista:
info = []
for i in np.arange(contador):
    imagen = Image.open(r'/home/mint/Desktop/imagen'+str(i)+'.jpg')
    
    #Recorto en la seccion de la fecha
    box = (32,354 , 250, 400)
    cropped = imagen.crop(box)
    contraste = ImageEnhance.Contrast(cropped).enhance(2)
    
    #Extraigo el contenido de la imagen
    fecha = pytesseract.image_to_string(contraste)
    
    #Recorto en la seccion de los datos
    box = (32,320 , 1120, 945)
    cropped = imagen.crop(box)
    contraste = ImageEnhance.Contrast(cropped).enhance(2)
    
    #Extraigo el contenido de la imagen
    text = pytesseract.image_to_string(contraste)
    
    #Busco en el texto los codigos que me interesan y guardo la informacion en
    #la lista 'info'
    Lista = ["0300"]
    for codigo in Lista:
        if codigo in text:
            suma=0
            inicio=0
            while inicio >= 0:
                inicio = text[suma:].find(codigo)          #Ubico el inicio de la linea
                fin = text[suma + inicio:].find("\n")      #Ubico el fin de la linea
                if inicio<0:
                    break
                info.append("Pagina "+str(i+1).zfill(2)+" "+ fecha[:fecha.find("\n")]
                             +" "+ text[suma+inicio:suma+inicio+fin])
                suma += inicio+1
                
        else:
            print("No se encontro el codigo ", codigo, " en la pagina ", i+1, "\n")
    
    imagen.close()
    ubicacion = os.path.join(r"/home/mint/Desktop/",
                             "imagen"+str(i)+".jpg")
    os.remove(ubicacion)

for i in range(len(info)):
    print(info[i])

"""
#Borro las imagenes creadas:
ubicacion = os.path.join(r"/home/mint/Desktop/", "imagen0.jpg")
os.remove(ubicacion)
"""
