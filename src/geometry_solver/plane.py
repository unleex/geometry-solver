import itertools

from geometry_solver.models import basic_objects


class Plane:

    def __init__(self) -> None:
        self.points: list[basic_objects.Point] = []
        self.angles: dict[
            tuple[
                "basic_objects.Point",
                "basic_objects.Point",
                "basic_objects.Point"
                ],
            basic_objects.Angle
            ] = {}
    
    def angle(
            self,
            p1: "basic_objects.Point",
            p2: "basic_objects.Point", 
            p3: "basic_objects.Point",
            degrees: float | None = None
            ):
        for points_perm in itertools.permutations((p1,p2,p3)):

            if points_perm in self.angles:
                return self.angles[(points_perm)] # type: ignore[index]
                    
        self.angles[(p1, p2, p3)] = basic_objects.Angle(
                self, p1, p2, p3, degrees
            )