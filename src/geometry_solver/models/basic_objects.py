from geometry_solver.core import core
from geometry_solver.utils import naming, utils


class Point(core.BaseObject):
    """
    A class representing a point in a 2D space.

    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """
        
    def __init__(self, name: str, plane: "core.Plane", xy: tuple[int | None, int | None] | None = None):
        """
        Initializes a Point object.

        Parameters:
            xy (tuple[int, int] | None): 
            A tuple containing the x and y coordinates of the point.
            If None, the point is considered undefined.
        """
        assert name not in naming.existing_point_names, f"Point {name} already exists!"
        # XXX: maybe allow it somehow?
        assert len(name) == 1 and name.isalpha(), "Point must be named as letter"
        naming.existing_point_names.append(name)
        super().__init__(name=name, plane=plane)
        if xy is None:
            xy = (None, None)
        xname, yname = naming.get_point_xy_name(self)
        self.x = core.BaseObject(value=xy[0], name=xname, plane=plane)
        self.y = core.BaseObject(value=xy[1], name=yname, plane=plane)


class LineSegment(core.BaseObject):
    """
    Represents a line segment defined by two points.

    Attributes:
        p1 (Point): The first point of the line segment.
        p2 (Point): The second point of the line segment.
    """
    def __init__(self, plane: "core.Plane", p1: Point, p2: Point, distance: float | None = None):
        """
        Parameters:
        p1 (Point): The first point of the line segment.
        p2 (Point): The second point of the line segment.
        """
        if ord(p1.name) > ord(p2.name):
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2
        super().__init__(
            name=naming.get_line_segment_name(self),
            plane=plane, 
            value=distance)
        self.intersections: dict[LineSegment, Angle] = {}

    def get_distance(self):
        """
        Calculate the distance between two points.

        Returns:
            float: The distance between point p1 and point p2.

        Raises:
            AssertionError: If the object is not defined.
        """
        return utils.get_distance(self.p1, self.p2)

    def add_point(self, point: Point):
        point in self.as_new_relation

    def start(self):
        return self.p1
    
    def end(self):
        return self.p2

    def ccw(self, A: Point, B: Point, C: Point) -> bool:
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    def intersects(self, other: "LineSegment") -> bool:
        A, B = self.p1, self.p2
        C, D = other.p1, other.p2
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)


class Angle(core.BaseObject):
    """
    Represents an acute angle between two line segments.
    Attributes:
        line1 (LineSegment): The first line segment.
        line2 (LineSegment): The second line segment.
        degrees (float | None): The measure of the angle in degrees, if defined.
    """

    def __init__(self, plane: "core.Plane", p1: Point, p2: Point, p3: Point, degrees: float | None = None):
        """
        Args:
        line1 (LineSegment): The first line segment.
        line2 (LineSegment): The second line segment.
        degrees (float, optional): The measure of the angle in degrees if defined. Defaults to None.
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        super().__init__(
            name=naming.get_angle_name(self),
            plane=plane,
            value=degrees
            )
        self.degrees = degrees