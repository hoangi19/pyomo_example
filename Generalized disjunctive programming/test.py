from pyomo.environ import *
from pyomo.gdp import *

m = ConcreteModel()
m.s = RangeSet(4)
m.ds = RangeSet(2)
m.d = Disjunct(m.s)
m.djn = Disjunction(m.ds)
m.djn[1] = [m.d[1], m.d[2]]
m.djn[2] = [m.d[3], m.d[4]]
m.x = Var(bounds=(-2, 10))
m.d[1].c = Constraint(expr=m.x >= 2)
m.d[2].c = Constraint(expr=m.x >= 3)
m.d[3].c = Constraint(expr=m.x <= 8)
m.d[4].c = Constraint(expr=m.x == 2.5)
m.o = Objective(expr=m.x)
# Add the logical proposition
m.p = LogicalConstraint(
   expr=m.d[1].indicator_var.implies(m.d[4].indicator_var))
# Note: the implicit XOR enforced by m.djn[1] and m.djn[2] still apply
# Convert logical propositions to linear algebraic constraints
# and apply the Big-M reformulation.
TransformationFactory('core.logical_to_linear').apply_to(m)
TransformationFactory('gdp.bigm').apply_to(m)
# Before solve, Boolean vars have no value
Reference(m.d[:].indicator_var).display()
# Solve the reformulated model and update the Boolean variables
# based on the algebraic model results
run_data = SolverFactory('glpk').solve(m)
Reference(m.d[:].indicator_var).display()
m.display()