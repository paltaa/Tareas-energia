from pyomo.environ import *
infinity = float('inf')

model = AbstractModel()

#Sets ###########################
# Foods
model.F = Set()
# Nutrients
model.N = Set()

#Parameters######################
# Cost of each food
model.c    = Param(model.F, within=PositiveReals)
# Amount of nutrient in each food
model.a    = Param(model.F, model.N, within=NonNegativeReals)
# Lower and upper bound on each nutrient
model.Nmin = Param(model.N, within=NonNegativeReals, default=0.0)
model.Nmax = Param(model.N, within=NonNegativeReals, default=infinity)
# Volume per serving of food
model.V    = Param(model.F, within=PositiveReals)
# Maximum volume of food consumed
model.Vmax = Param(default=75.0, within=PositiveReals, mutable=True)

#Variables#######################
# Number of servings consumed of each food
model.x = Var(model.F, within=NonNegativeReals)

#Objective Function
# Minimize the cost of food that is consumed
def cost_rule(model):
    return sum(model.c[i]*model.x[i] for i in model.F)
model.cost = Objective(rule=cost_rule)

#Constraints
# Limit nutrient consumption for each nutrient
def nutrient_rule_min(model, j):
    return model.Nmin[j] <= sum(model.a[i,j]*model.x[i] for i in model.F)
model.nutrient_limit_min = Constraint(model.N, rule=nutrient_rule_min)

def nutrient_rule_max(model, j):
    return sum(model.a[i,j]*model.x[i] for i in model.F) <= model.Nmax[j]
model.nutrient_limit_max = Constraint(model.N, rule=nutrient_rule_max)

# Limit the volume of food consumed
def volume_rule(model):
    return sum(model.V[i]*model.x[i] for i in model.F) <= model.Vmax
model.volume = Constraint(rule=volume_rule)