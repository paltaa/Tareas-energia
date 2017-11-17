#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyomo.environ import *
infinity = float('inf')
#Constantes a manipular
VOLL=500
Hh=8760/670
model = AbstractModel()
TAX=80
#Sets ###########################
# Cargando Demanda x hora
model.h = RangeSet(1, 670)
# Cargando tabla de generadores incluida eolica
model.E = Set()
# Cargando tabla de generadores sin incluir eolica
model.A= Set()

#Parametros#####################
# Costo de los generadores
model.MCi = Param(model.E)

# capacidad maxima de los generadores
model.Ki  = Param(model.E)

#factor de planta anual maximo 
model.MCFi=  Param(model.E)

#costo inversion en tecnologias
model.Ii= Param(model.E)
#Tasa falla del generador
model.FOR=Param(model.E)
#emisiones por tecnologia
model.Ei=Param(model.E)
#Demanda
model.demanda=Param(model.h)

#PEFIL TCHAMA
model.tchama=Param(model.h)

#######FIN PARAMETROS Y SETS DE DATOS ###########
#Variable de desicion ( Cuanto producir por hora y por generador)
model.x=Var(model.E ,model.h, within=NonNegativeReals)
#vARIABLE DE HOLGURA
model.u=Var(model.h, within=NonNegativeReals)

#variables de inversion en tecnologias

model.y=Var(model.E, within=NonNegativeReals)

#minimizar funcion de costo de los generadores

def funcion_costo(model):
    return sum(model.Ii[i]*model.y[i] for i in model.E)+ Hh*sum(sum( model.MCi[i] * model.x[i,h] +(model.Ei[i]*TAX)*model.x[i,h] for i in model.E)+ VOLL * model.u[h] for h in model.h )
model.cost=Objective(rule=funcion_costo, sense=minimize)

#Satisfaccion de la demanda
def satisfaccion_demanda(model, h):
    return sum(model.x[i,h]   for i in model.E) + model.u[h]  == model.demanda[h]*2
model.satisfaccion_demanda = Constraint(model.h, rule=satisfaccion_demanda)

#ajustar capacidad de generadores con FOR todos menos eolica

def ajustar_generadores(model,i ,h):
    return model.x[i,h] <= (model.Ki[i]+model.y[i])*(1-model.FOR[i])
model.ajuste = Constraint(model.A, model.h, rule=ajustar_generadores)

#SOLO PARA LA TECNOLOGIA EOLICA

def ajustar_generadores_eolica(model,h):
    return model.x['Wind',h] <= (model.Ki['Wind']+model.y['Wind'])*(1-model.FOR['Wind'])*model.tchama[h]
model.ajuste_eolica = Constraint(model.h, rule=ajustar_generadores_eolica)


#limitantes maximos de factores de planta
def limitantes_planta(model, i):
    return sum(Hh*model.x[i,h] for h in model.h)<=model.MCFi[i]*(model.Ki[i]+model.y[i])*8760
model.limite = Constraint(model.E, rule=limitantes_planta)


datos = DataPortal()
datos.load(filename = "tarea2.dat")
opt = SolverFactory("glpk")
instance = model.create_instance(datos)
instance.dual = Suffix(direction=Suffix.IMPORT)
results = opt.solve(instance)
print("%f") % (instance.cost())


#obtener generacion e inversion por tecnologia
generacion={}
emicionesTotales=0
InversionesConvencionales=0
print("tecnologia, Energia generada, inversion en MW, emiciones por tecnologia ")
for i in instance.E:
    emiciones=0
    gen=0
    for h in instance.h:
        gen=gen+instance.x[i,h].value
        #generacion[i]=generacion[i]+instance.x[i,h].value
        emiciones=emiciones+instance.Ei[i]*instance.x[i,h].value*Hh
    emicionesTotales=emicionesTotales+emiciones
    print("%s, %f, %f, %f") % (i,gen+instance.y[i].value, instance.y[i].value, emiciones)
    
    
    
    
print("TAX [$/Ton CO2], Costo Total [$], inv Convencionales[MW], Inv. Hydro[MW], Inv. Wind[MW], Emisiones Totales [M Ton CO2]")    
print("%i, %f, %f, %f, %f, %f") % (TAX, instance.cost(), instance.y['Diesel'].value+instance.y['CCGT'].value+instance.y['Coal'].value, instance.y['Hydro'].value, instance.y['Wind'].value, emicionesTotales)
#obtener factores de planta
#cf={}    
#    
#for i in instance.E:
#    cf[i]=0
#    final=sum(instance.x[i,h].value for h in instance.h)/instance.Ki[i]*instance.MCFi[i]   #(Hh*100)
#    print("tecnologia: %s y cf: %f") % (i, final)
#    
#    
#    
#Precios por hora en $/MWh
#precios = {}
#
#for h in instance.h:
#	precios[h]=instance.dual[instance.satisfaccion_demanda[h]]/Hh
#
#utilidades = {}
#    
#for i in instance.E:
#	utilidades[i] = round(sum((precios[h]-instance.MCi[i])*instance.x[i,h].value*Hh for h in instance.h)/1000000,1)
#	print(i, round(sum(instance.x[i,h].value*Hh for h in instance.h)/1000,1), round(sum(instance.x[i,h].value*Hh for h in instance.h)/(8760*instance.Ki[i]),3), utilidades[i])
#
#print(" ")
#print("Precio promedio", round(sum(precios[h]*instance.demanda[h]*Hh for h in instance.h)/sum(Hh*instance.demanda[h]for h in instance.h),1))
#
