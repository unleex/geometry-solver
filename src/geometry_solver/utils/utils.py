from geometry_solver.models import basic_objects, polygons
from geometry_solver.core import core
import sympy


def get_distance(p1: "basic_objects.Point", p2: "basic_objects.Point"):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

