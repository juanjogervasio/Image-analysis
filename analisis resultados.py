#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 16:47:09 2022

@author: mint
"""

#Lector de los resultados de recibos.py
#Separo los resultados segun el codigo

#Voy a buscar los codigos en la lista:
Lista = ["0300", "2760", "2762", "2554", "2555", "2665", "2680"]

for i in range(1,6,1):
    with open("Lectura Recibo" + str(i) + ".txt", "r") as texto:
        contenido = texto.readlines()
        
        #Imprimo primera linea en los archivos de salida
        for codigo in Lista:
            salida = open("Resultados codigo " + codigo + ".txt", "a")
            print("  ","\n", contenido[0], file=salida)
            salida.close()
        
        #Busco las lineas que contengan cada codigo y las imprimo donde corresp.
        for j in range(len(contenido)):
            for codigo in Lista:
                if contenido[j].find(codigo) > 0:
                    with open("Resultados codigo " + codigo + ".txt", "a") as salida:
                        salida.write(contenido[j])
    