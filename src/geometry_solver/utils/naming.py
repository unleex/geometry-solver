from geometry_solver.models import basic_objects, polygons
from geometry_solver.core import core

existing_point_names: list[str] = []

def get_new_point_name():
       # XXX: avoid sorting each time
       existing_point_names.sort()
       last_name = existing_point_names[-1]
       # TODO: handle exhaustment of alphabet
       return chr(ord(last_name[-1]) + 1)

def get_line_segment_name(line_segment: "basic_objects.LineSegment"):
       return f"{line_segment.start()}{line_segment.end()}"

def get_angle_name(angle: "basic_objects.Angle"):
       return f"{angle.p1}{angle.p2}{angle.p3}"

def get_point_xy_name(point: "basic_objects.Point"):
        return point.name + "x", point.name + "y"

def get_polygon_name(polygon: "polygons.Polygon"):
        return ''.join([vertex.name for vertex in polygon.vertices])

def get_perpendicular_bisector_edge_points(edge_to: "basic_objects.LineSegment"):
        return f"pb{edge_to.name}s", f"pb{edge_to.name}e"

def get_circumcircle_name(polygon: "polygons.Polygon"):
    return f"o{polygon.name}"