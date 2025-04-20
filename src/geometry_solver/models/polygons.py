from geometry_solver.core import core
from geometry_solver.models import basic_objects, circle
from geometry_solver.utils import utils, naming
from geometry_solver.definitions import definitions


class Polygon(core.BaseObject):
    """
    A class to represent a polygon.

    Attributes
    ----------
    vertices : list[basic_objects.Point]
        A list of points representing the vertices of the polygon.
    edges : list[basic_objects.LineSegment]
        A list of line segments representing the edges of the polygon."
    """

    def __init__(
            self, 
            plane,
            vertices: list[basic_objects.Point],
            is_cyclic: bool | None = None,
            inscribed_in: circle.Circle | None = None
        ):
        """
        Initialize a Polygon object.

        Args:
            vertices (list[basic_objects.Point]): A list of Point objects representing the vertices of the polygon.

        Attributes:
            vertices (list[basic_objects.Point]): The vertices of the polygon.
            edges (list[basic_objects.LineSegment]): The edges of the polygon, created by connecting consecutive vertices.

        The polygon is considered defined if all its vertices are defined.
        """
        if not is_cyclic:
            assert not inscribed_in, "Non-cyclic polygons cannot be inscribed."
        self.vertices = vertices
        super().__init__(
            name=naming.get_polygon_name(self),
            plane=plane
            )
        self.edges: list[basic_objects.LineSegment] = []
        for vertex1, vertex2 in zip(vertices, vertices[1:] + [vertices[0]]):
            self.edges.append(basic_objects.LineSegment(plane, vertex1, vertex2))
        self.angles = []
        self.plane = plane
        for vertex_i in range(2, len(vertices)):
            self.angles.append(plane.angle(
                vertices[vertex_i - 2],
                vertices[vertex_i - 1],
                vertices[vertex_i]
                ))
        self.is_cyclic = is_cyclic
        self.inscribed_in: circle.Circle = inscribed_in

        if self.inscribed_in:
            self.is_cyclic = True
            self.build_circumcircle()
        
        
    def build_perpendicular_bisector(self, to_side: basic_objects.LineSegment):
        if to_side not in self.edges:
            raise ValueError(
                f"{to_side} is not in {self}!")
        start_point, end_point = naming.get_perpendicular_bisector_edge_points(object=to_side)
        to_point = basic_objects.Point(name=start_point)
        to_side.add_point(to_point)
        to_side_idx = self.edges.index(to_side)
        from_side = self.edges[to_side_idx + len(self.edges) // 2]
        if len(self.edges) % 2 == 0:
            from_point = basic_objects.Point(name=end_point)
            from_side.add_point(from_point)
        else:
            from_point = from_side.end()
        
        return basic_objects.LineSegment(
            plane=self.plane,
            p1=from_point, 
            p2=to_point
            )

    def build_circumcircle(
            self, 
            check_if_possible: bool = False,
            radius = None
            ):
        # XXX: warn if already inscribed?
        if not check_if_possible:
            self.is_cyclic = True
        else:
            assert self.is_cyclic, "Non-cyclic polygons cannot be inscribed."
        center = basic_objects.Point(
            naming.get_new_point_name(),
            plane=self.plane)
        circumcircle = circle.Circle(
            name=naming.get_circumcircle_name(self),
            center=center,
            plane=self.plane,
            inscribed_polygons=[self],
            radius=radius
        )
        self.inscribed_in = circumcircle
        return circumcircle
        # prev = None
        # for to_edge in self.edges:
        #     bisector = self.build_perpendicular_bisector(to_edge)
        #     if prev is None:
        #         continue
        #     if bisector.intersects(prev):
        #         self.is_cyclic = False
        #         return None
        #     prev = bisector
                    
  
class Triangle(Polygon):

    def __init__(
            self, 
            plane,
            vertices: list[basic_objects.Point],
            inscribed_in: circle.Circle | None = None            
            ):
        
        if len(vertices) != 3:
            raise ValueError(
                f"Triangle must have 3 vertices. Found {len(vertices)}"
                )
        super().__init__(
            plane, 
            vertices,
            is_cyclic=True,
            inscribed_in=inscribed_in
            )


class RegularTriangle(Triangle):

    def __init__(
            self, 
            plane,
            vertices: list[basic_objects.Point],
            side_length: float | None = None
            ):
        
        super().__init__(plane, vertices)
        if not side_length:
            return
        for edge in self.edges:
            if not edge.is_constant():  
                edge.set_value(side_length)
            assert edge is None or edge.value == side_length
        self.edges[0].as_new_relation == self.edges[1]
        self.edges[1].as_new_relation == self.edges[2]
    
    def get_side(self):
        return self.edges[0]

    def build_circumcircle(
            self,
            check_if_possible = False,
            radius = None
            ):
        super().build_circumcircle(
            check_if_possible,
            radius=radius
            )
        self.inscribed_in.add_definition(
            definitions.circumcirle_radius_of_regular_triangle(
            circumcircle=self.inscribed_in,
            tri=self
        ))
    

def triangle(
        plane, 
        vertices: list[basic_objects.Point]
    ):
    triangle = Triangle(
        plane,
        vertices
    )
    if triangle.vertices[0] == triangle.vertices[1] \
    and triangle.vertices[1] == triangle.vertices[2]:
        triangle = RegularTriangle(
            plane=plane,
            vertices=vertices
        )
    return triangle