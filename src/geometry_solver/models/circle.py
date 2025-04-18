from geometry_solver.core import core
from geometry_solver.models import basic_objects, polygons


class Circle(core.BaseObject):

    def __init__(
            self, 
            name: str,
            plane, 
            center: "basic_objects.Point",
            radius = None,
            inscribed_polygons: list["polygons.Polygon"] = None
        ):
        super().__init__(name, plane, radius)
        self.radius = radius
        self.center = center
        self.inscribed_polygons = inscribed_polygons if inscribed_polygons else []
    
    def inscribe(self, polygon: "polygons.Polygon"):
        self.inscribed_polygons.append(polygon)
        polygon.inscribed_in = self