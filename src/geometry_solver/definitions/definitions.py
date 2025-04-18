from geometry_solver.models import polygons, circle, basic_objects
from geometry_solver.core import core
import sympy
import uuid

# XXX: should it take edges as argument?
# should only one edge be required to be passed?
def circumcirle_radius_of_regular_triangle(
        tri: "polygons.RegularTriangle"
):
    def _circumcirle_radius_of_regular_triangle(
           args
    ):
        tri: "polygons.RegularTriangle" = args[0]
        return core.BaseObject.from_sympy(
            plane=tri.plane,
            expr=tri.get_side().value / sympy.sqrt(3)
        )
    
    return core.Definition(
        depends_on=[tri],
        define_func=_circumcirle_radius_of_regular_triangle
    )