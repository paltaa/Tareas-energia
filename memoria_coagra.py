#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import csv

k={}


#leer el archivo csv por fila
with open('Final20102016CSV.csv', 'rU') as csvfile:
    readCSV = csv.reader(csvfile)
    i=0
    for row in readCSV:
 
        k[i]=str(row)
        i=i+1

#separar las filas en 4 columnas distintas
for i in xrange(0,len(k)) :       
    k[i]=k[i].split(";")
    k[i][0]=k[i][0][2:]
    #print(k[i][0])
    k[i][3]=k[i][3][:-2]
    
#verificar q no haya errores en los numeros
"""
for i in xrange(len(k)):
    for j in xrange(len(k[1])):
        print(k[i][j])
"""

#sumamos las files repetidas por dia y producto
filasSumadas=0
for i in xrange(len(k)):
    for j in xrange(len(k)):
        if(k[i][0]==k[j][0] and k[i][1]==k[j][1] and k[i][2]==k[j][2]):
            k[i][3]=k[i][3]+k[j][3]
            filasSumadas=filasSumadas+1
            for h in xrange(3):
                 k[j][h]=0
print("filas sumadas=")
print(filasSumadas)

for i in xrange(len(k)):
    if(k[i][0]==0 and k[i][1]==0 and k[i][2]==0):
        k.pop(i)
        
with open ("final.csv", 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(k)

