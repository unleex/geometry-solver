from __future__ import annotations
import typing
import uuid
if typing.TYPE_CHECKING:
    from geometry_solver import plane

import sympy
import sympy.core

class RelationSetter:

    def __init__(self, obj: BaseObject):

        self.obj = obj
    def __eq__(self, other: BaseObject): # type: ignore[override] # why only here though?
        self.obj.relations.update(other.relations)
        other.relations = self.obj.relations
        self.obj.value = other.value
        self.obj.relations["eq"].append(other)

    def __lt__(self, other: BaseObject):
        self.obj.relations["lt"].append(other)

    def __le__(self, other: BaseObject):
        self.obj.relations["lt"].append(other)

    def __gt__(self, other: BaseObject):
        self.obj.relations["lt"].append(other)

    def __ge__(self, other: BaseObject):
        self.obj.relations["lt"].append(other)

    def __contains__(self, other: BaseObject):
        return self.obj.relations["contains"].append(other)

class BaseObject():
    """
    Base class that offers basic operations like greater/less comparison. 
    This object imitates a variable, whose value can be unknown.
    """
    def __init__(
            self, 
            name: str, 
            plane: "plane.Plane", 
            value: float | None = None, 
            definitions: list["Definition"] | None = None
        ):
        self.name = name
        self.plane = plane
        self.relations: dict[str, list[BaseObject]] = {
            "gt": [], "ge": [], "lt": [], "le": [], "eq": [], "contains": []
        }
        self.value: sympy.Symbol | sympy.Float
        if value:
            self.value = sympy.core.Float(value)
        else:
            self.value = sympy.core.Symbol(name)
        if definitions:
            self.definitions = definitions
        else:
            self.definitions = []
        
        self.as_new_relation = RelationSetter(self)

    @classmethod
    def from_sympy(
        cls,
        expr: sympy.Expr,
        plane: "plane.Plane"
    ):
        self = cls(
            name=str(uuid.uuid1()),
            plane=plane
        )
        self.set_value(expr)
        return self

    
    def __lt__(self, other: BaseObject) -> bool | None:
        if other.value in self.relations["lt"]:
            return True
        elif other.value in self.relations["ge"]:
            return False
        return None

    def __le__(self, other: BaseObject) -> bool | None:
        if other.value in self.relations["le"]:
            return True
        elif other.value in self.relations["gt"]:
            return False
        return None

    def __gt__(self, other: BaseObject) -> bool | None:
        if other.value in self.relations["gt"]:
            return True
        elif other.value in self.relations["le"]:
            return False
        return None

    def __ge__(self, other: BaseObject) -> bool | None:
        if other.value in self.relations["ge"]:
            return True
        elif other.value in self.relations["lt"]:
            return False
        return None
    
    def __contains__(self, other: BaseObject) -> bool | None:
        return other in self.relations["contains"]
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):  
        return repr(self.value)

    def set_value(self, value: float | sympy.Expr):
        if isinstance(value, float):
            value = sympy.Float(value)
        self.value = value
    

    # basically, the idea of the project
    def define(self):
        for definition in self.definitions:
            result = definition.define()
            if result is not None and result.value.is_constant():
                self.set_value(result)
                return result
            
    def add_definition(self, definition: "Definition"):
        self.definitions.append(definition)

class Definition:

    def __init__(
            self, 
            depends_on: typing.Sequence[BaseObject], 
            define_func: typing.Callable[..., BaseObject]
        ):
        
        self.depends_on = depends_on
        self.define_func = define_func
    
    def define(self):
        result = self.define_func(self.depends_on)
        if result.value.is_constant(): 
            return result
        for dependent in self.depends_on:
            dependent.define()

        result = self.define_func(self.depends_on)
        if result.value.is_constant(): 
            return result
        return None