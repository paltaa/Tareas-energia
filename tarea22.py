#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyomo.environ import *
infinity = float('inf')
#Constantes a manipular
model = AbstractModel()
#Sets ###########################

VOLL=500
# Cargando Demanda x hora
model.h = Set()
# Cargando tabla de generadores incluida solar
model.A = Set()
# Cargando tabla de generadores sin incluir solar
model.B= Set()

#Parametros#####################
# Costo de los generadores
model.MCi = Param(model.A)

# capacidad maxima de los generadores
model.Ki  = Param(model.A)
#capacidad Solar
model.Solar=Param(model.h ,within=Reals)
#factor de planta anual maximo 
model.MCFi=  Param(model.A)

#Tasa falla del generador
model.FOR=Param(model.A)
#emisiones por tecnologia

#Demanda
model.demanda=Param(model.h)



#######FIN PARAMETROS Y SETS DE DATOS ###########
#Variable de desicion ( Cuanto producir por hora y por generador)
model.x=Var(model.A ,model.h, within=NonNegativeReals)
#vARIABLE DE HOLGURA
model.u=Var(model.h, within=NonNegativeReals)

###FIN VARIABLES DE DESICION

#minimizar funcion de costo de los generadores

def funcion_costo(model):
    return sum(sum (model.x[i,h]*model.MCi[i]for i in model.E) + VOLL*model.u[h] for h in model.h)
model.cost=Objective(rule=funcion_costo, sense=minimize)

#Satisfaccion de la demanda
def satisfaccion_demanda(model, h):
    return sum(model.x[i,h]   for i in model.A) + model.u[h]  == model.demanda[h]
model.satisfaccion_demanda = Constraint(model.h, rule=satisfaccion_demanda)

#CAPACIDAD MINIMA DE GENERADOR 'COAL'
def max_coal(model,h):
    return model.x['Coal',h]>=200
model.max_coal=Constraint(model.h, rule=max_coal)

#ajustar capacidad de generadores con FOR todos menos solar

def ajustar_generadores(model,i ,h):
    return model.x[i,h] <= (model.Ki[i])*(1-model.FOR[i])
model.ajustar_generadores = Constraint(model.B, model.h, rule=ajustar_generadores)

#ajustar generador solar
def ajustar_generador_solar(model ,h):
    return model.x['Solar',h] <= (model.Ki['Solar'])*(1-model.FOR['Solar'])*model.Solar[h]
model.ajustar_generador_solar = Constraint(model.h, rule=ajustar_generador_solar)
#Restricciones de rampa subida y bajada

#def rampa_subida(model, h):
#    return model.x['Coal',h]-model.x['Coal',h-1]<=50
#model.rampa_subida = Constraint(model.h, rule=rampa_subida)
#
#
#def rampa_bajada(model, h):
#    return model.x['Coal',h-1] - model.x['Coal',h]<=50
#model.rampa_bajada = Constraint(model.h, rule=rampa_bajada)


print(model.Solar)
datos = DataPortal()
datos.load(filename = "tarea2c.dat")
opt = SolverFactory("glpk")
instance = model.create_instance(datos)
instance.dual = Suffix(direction=Suffix.IMPORT)
results = opt.solve(instance)
print("%f") % (instance.cost())
