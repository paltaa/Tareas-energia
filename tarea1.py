#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 23:45:12 2017

@author: juan
"""
from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import energia1


# Create a solver
opt = SolverFactory('glpk')

data = DataPortal()
data.load(filename='energia1.dat')

# Create a model instance and optimize
instance = energia1.model.create_instance(data)
instance.dual = Suffix(direction=Suffix.IMPORT)

results = opt.solve(instance)

print " "
print "************** Resultados *************"
print "Funcion objetivo", instance.cost()

#Imprimir variables
#print " "
print "Variables"
for i in instance.E:
    for h in instance.D:
	print f, instance.x[i,h].value

#print " "
#print "Variabl dual de restriccion de volumen"
#print instance.dual[instance.volume]
#
#print " "
#print "Variabl dual de restricciones de nutrientes minimos"
#for j in instance.N:
#	print j, instance.dual[instance.nutrient_limit_min[j]]

#print " "
#print "Sensibilidad respecto a Vmax"
#Mutar un parametro y volver a resolver, ojo que debe ser mutable

#for valores in [30,40,50,60]:
#	#re definir el valor de Vmax
#	instance.Vmax.value=valores
#
#	#volver a resolver
#	results = opt.solve(instance)
#
#	#imprimir vmax y funcion objetivo
#	print valores, instance.cost()