from geometry_solver.models import polygons, circle, basic_objects
from geometry_solver.core import core
import sympy

# XXX: should it take edges as argument?
# should only one edge be required to be passed?

def circumcirle_radius_of_regular_triangle(
        circumcircle: "circle.Circle",
        tri: "polygons.RegularTriangle"
):  
    return core.BaseDefinition(
        target=circumcircle,
        expression= tri.get_side()/sympy.sqrt(3)
    )