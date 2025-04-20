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

class BaseObject(sympy.Symbol):
    """
    Base class that offers basic operations like greater/less comparison. 
    This object imitates a variable, whose value can be unknown.
    """
    # XXX: this initialization is NOT fine. how to make it properly?
    def __new__(
            cls, 
            *args, **kwargs
        ):
        return super().__new__(cls, str(uuid.uuid1()))
    
    def __init__(
            self, 
            name: str, 
            plane: "plane.Plane", 
            value: float | None = None, 
            definitions: list["BaseDefinition"] | None = None
        ):
        self.name = name
        self.plane = plane
        self.relations: dict[str, list[BaseObject]] = {
            "gt": [], "ge": [], "lt": [], "le": [], "eq": [], "contains": []
        }
        self.value: sympy.Expr | sympy.Float | None = (
            sympy.Float(value) if value is not None else None
        )
        if definitions:
            self.definitions = definitions
        else:
            self.definitions = []
        
        self.as_new_relation = RelationSetter(self)

    
    def __lt__(self, other) -> bool | None:
        if not isinstance(other, BaseObject):
            return super().__lt__(other)
        if other.value in self.relations["lt"]:
            return True
        elif other.value in self.relations["ge"]:
            return False
        return None

    def __le__(self, other) -> bool | None:
        if not isinstance(other, BaseObject):
            return super().__lt__(other)
        if other.value in self.relations["le"]:
            return True
        elif other.value in self.relations["gt"]:
            return False
        return None

    def __gt__(self, other) -> bool | None:
        if not isinstance(other, BaseObject):
            return super().__lt__(other)
        if other.value in self.relations["gt"]:
            return True
        elif other.value in self.relations["le"]:
            return False
        return None

    def __ge__(self, other) -> bool | None:
        if not isinstance(other, BaseObject):
            return super().__lt__(other)
        if other.value in self.relations["ge"]:
            return True
        elif other.value in self.relations["lt"]:
            return False
        return None
    
    def __contains__(self, other) -> bool | None:
        return other in self.relations["contains"]
    

    def set_value(self, value: sympy.Expr):
        self.value = value
    

    # basically, the idea of the project
    def define(self):
        for definition in self.definitions:
            result = definition.define()
            if result is not None and is_expression_constant(result):
                self.set_value(expression_as_constant(result))

                return result
            
    def add_definition(self, definition: "BaseDefinition", reverse_definitions: bool = True):
        self.definitions.append(definition)
        if reverse_definitions:
            assign_reexpressed_definitions(
                right_expression=definition.expression,
                target=self
            )
    def is_defined(self):
        return self.value is not None
    
    def __str__(self):
        ret = self.name
        if self.is_defined():
            ret += f'(={self.value})'
        return ret

# TODO: allow reverse definitions and simplifications like back in sympy
class BaseDefinition:

    def __init__(
            self, 
            target: BaseObject,
            expression: sympy.Expr,
        ):       

        self.target = target
        self.expression = expression
        self._is_tried = False
        self.build_equation()

    # TODO: deal with sets that contain more than one element,
    # e.g. when colving quadratic eqs
    def define(self) -> typing.Any | None:
        # avoid circular definition attempts
        if self.tried:
            return None
        self.tried = True
        result = sympy.solve(self.equation, self.target)[0]
        if is_expression_constant(result): 
            return result
        depends_on = set(get_objects_from_expression(self.expression))
        depends_on -= set((self.target,))
        for dependent in depends_on:
            dependent.define()

        # attempt again, if anything was defined
        self.build_equation()
        result = sympy.solve(self.equation, self.target)[0]
        self.tried = False
        if is_expression_constant(result):
            return result
        return None

    def build_equation(self):
        self.equation = sympy.Eq(
            self.target,
            self.expression
        )

    @property
    def is_tried(self):
        return self._is_tried

    @is_tried.setter # type: ignore[attr-defined] # poor mypy doesn't know properties
    def tried(self, value: bool):
        self._is_tried = value
    
    def __str__(self):
        return f"Definition({self.expression})"
    

def get_reexpressed_definitions(
        right_expression: sympy.Expr,  
        target: BaseObject,
):  
    reexpressed_definitions: dict[BaseObject, BaseDefinition] = {}
    variables = get_objects_from_expression(right_expression)
    expr = (target - right_expression)
    for newtarget in variables:
        expr = (target - right_expression)
        newexpr = sympy.solve(
            expr,
            newtarget
        )
        # TODO: handle multiple solutions
        newexpr = newexpr[0]
        newdef = BaseDefinition(
            target=newtarget,
            expression=newexpr
            )
        reexpressed_definitions[newtarget] = newdef
    return reexpressed_definitions

def assign_reexpressed_definitions(
        right_expression: sympy.Expr,
        target: BaseObject
        ):
    reexpressed_definitions = get_reexpressed_definitions(
        right_expression=right_expression,
        target=target
    )
    for target, definition in reexpressed_definitions.items():
        target.add_definition(definition, reverse_definitions=False)

def get_objects_from_expression(expression: sympy.Expr):
    return [atom for atom in expression.atoms() if isinstance(atom, BaseObject)]

def is_expression_constant(expr) -> bool:
    return all(
        var.is_defined() for var in get_objects_from_expression(expr)
    )

def expression_as_constant(expr: sympy.Expr) -> None | sympy.Expr:
    if not is_expression_constant(expr):
        return None
    variables = get_objects_from_expression(expr)
    for var in variables:
        expr = expr.subs(var, var.value) 
    return expr