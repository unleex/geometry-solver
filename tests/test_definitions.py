from geometry_solver.core.core import is_expression_constant
from geometry_solver.models import polygons, basic_objects
from geometry_solver.plane import Plane

def test_radius_to_regular_triangle_side():
    plane = Plane()
    a = basic_objects.Point("a", plane)
    b = basic_objects.Point("b", plane)
    c = basic_objects.Point("c", plane)
    tri = polygons.RegularTriangle(
        plane=plane,
        vertices=[a, b, c],
    )
    tri.build_circumcircle(radius=8)
    assert is_expression_constant(tri.get_side().define())
