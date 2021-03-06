#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 23:03:49 2017

@author: juan
"""

from pyomo.environ import *
infinity = float('inf')
model = AbstractModel()

#Sets ###########################
# Cargando Demanda x hora
# Cargando tabla de nodos generadores
model.A = Set()
# Cargando tabla de todos los nodos
model.B = Set()

#Parametros#####################
# Costo de los generadores
model.MCi = Param(model.B)

#Demanda
model.demanda=Param(model.A)

model.x=Var(model.B, within=NonNegativeReals)
model.fab=Var()
model.fbd=Var()
model.fdc=Var()
model.fbc=Var()
model.fca=Var()


def funcion_costo(model):
    return sum(model.x[i]*model.MCi[i]for i in model.B)
model.cost=Objective(rule=funcion_costo, sense=minimize)

def demanda_nodo_A(model):
    return model.x['A']+model.fca-model.fab==model.demanda['A']
model.demanda_nodo_A = Constraint(rule=demanda_nodo_A)

def demanda_nodo_B(model):
    return model.x['B']+model.fab-model.fbd-model.fbc==model.demanda['B']
model.demanda_nodo_B= Constraint(rule=demanda_nodo_B)

def demanda_nodo_C(model):
    return model.fbc+model.fdc-model.fca==model.demanda['C']
model.demanda_nodo_C = Constraint(rule=demanda_nodo_C)

def demanda_nodo_D(model):
    return model.x['D']+model.fbd-model.fdc==model.demanda['D']
model.demanda_nodo_D = Constraint(rule=demanda_nodo_D)
#restricciones capacidad fbc

def capacidad_fbc_top(model):
    return model.fbc <= 50
model.capacidad_fbc_top = Constraint(rule = capacidad_fbc_top)
def capacidad_fbc_bot(model):
    return -model.fbc <= 50
model.capacidad_fbc_bot = Constraint(rule = capacidad_fbc_bot)
#restricciones de capacidad fab

def capacidad_fab_top(model):
    return model.fab <= 100
model.capacidad_fab_top = Constraint(rule = capacidad_fab_top)

def capacidad_fab_bot(model):
    return -model.fab <= 100
model.capacidad_fab_bot = Constraint(rule = capacidad_fab_bot)
#restricciones de capacidad fbd

def capacidad_fbd_top(model):
    return model.fbd <= 100
model.capacidad_fbd_top = Constraint(rule = capacidad_fbd_top)

def capacidad_fbd_bot(model):
    return -model.fbd <= 100
model.capacidad_fbd_bot = Constraint(rule = capacidad_fbd_bot)
#restricciones de capacidad fdc

def capacidad_fdc_top(model):
    return model.fdc <= 100
model.capacidad_fdc_top = Constraint(rule = capacidad_fdc_top)

def capacidad_fdc_bot(model):
    return -model.fdc <= 100
model.capacidad_fdc_bot = Constraint(rule = capacidad_fdc_bot)

#restricciones de capacidad fca

def capacidad_fca_top(model):
    return model.fca <= 100
model.capacidad_fca_top = Constraint(rule = capacidad_fca_top)

def capacidad_fca_bot(model):
    return -model.fca <= 100
model.capacidad_fca_bot = Constraint(rule = capacidad_fca_bot)


def no_neg(model, i):
    return model.x[i] >= 0
model.no_neg = Constraint(model.B, rule=no_neg)


datos = DataPortal()
datos.load(filename = "tarea3a.dat")
opt = SolverFactory("glpk")
instance = model.create_instance(datos)
instance.dual = Suffix(direction=Suffix.IMPORT)
results = opt.solve(instance)
print("costo total: %f") % (instance.cost())

for i in instance.B:
    print instance.x[i],",", instance.x[i].value

print 'fab, ', instance.fab.value
print 'fbd, ', instance.fbd.value
print 'fdc, ', instance.fdc.value
print 'fbc, ', instance.fbc.value
print 'fca, ', instance.fca.value
print "Duals"
from pyomo.core import Constraint
for c in instance.component_objects(Constraint, active=True):
    print ("   Constraint "+str(c))
    cobject = getattr(instance, str(c))
    for index in cobject:
        print ("      ", index, instance.dual[cobject[index]])

