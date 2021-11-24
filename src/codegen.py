import re
from ast import AnnAssign, ClassDef, Index, Module, Name, Subscript, Tuple
from collections import defaultdict
from typing import Dict, List

import astor

from src.ordered_set import OrderedSet


def collect_types(data: dict) -> Dict[str, set]:
    """
    Turns values into types
    """
    types = defaultdict(set)  # type: ignore
    for k, v in data.items():
        if hasattr(v, "__len__") and not isinstance(v, str):
            types[k] = defaultdict(OrderedSet)
            for val in v:
                iterable_name = str(type(v).__name__).capitalize()
                #  Temp fix for 1 level nested dict
                if iterable_name == "Dict":
                    key = list(v.keys())[0]
                    value = list(v.values())[0]
                    types[k][iterable_name].add(type(key))
                    types[k][iterable_name].add(type(value))
                else:
                    types[k][iterable_name].add(type(val))
        else:
            types[k].add(type(v))
    return types


def reduce_types(data: Dict[str, set]) -> Dict[str, str]:
    """
    Flattens set of types to string of types
    # ToDO Handle nested dicts
    """
    types = dict()
    for k, v in data.items():
        if isinstance(v, dict):
            key = list(v)[0]
            vals = [val.__name__ for val in list(v[key])]
            joined = ", ".join(vals)

            #  Key is temp fix for nested dict
            if len(vals) > 1 and key != "Dict":
                joined = f"Union[{joined}]"
            types[k] = f"{key}[{joined}]"
        elif len(v) == 1:
            types[k] = list(v)[0].__name__
    return types


def create_single_annotation(target: str, annotation: str) -> AnnAssign:
    """
    Simple wrapper for generating AnnAssign
    """
    return AnnAssign(
        target=Name(id=target),
        annotation=Name(id=annotation),
        value=None,
        simple=1,
    )


def create_collection_annotation(
    target: str,
    collection: str,
    annotations: List[str],
) -> AnnAssign:
    """
    Simple wrapper for generating AnnAssign with Union types
    """
    _names = [Name(id=ann) for ann in annotations]
    if len(_names) > 1:
        index_value = Tuple(elts=_names)
    else:
        index_value = _names[0]  # type: ignore
    return AnnAssign(
        target=Name(id=target),
        annotation=Subscript(
            value=Name(id=collection),
            slice=Index(value=index_value),
        ),
        value=None,
        simple=1,
    )


TypedDictBase = Name(id="TypedDict")  # Created must inherit from TypedDict


def collect_annotations(types: Dict[str, str]) -> List[AnnAssign]:
    """
    Creates appropriate annotations single and union types
    """
    anns: List[AnnAssign] = []
    for k, v in types.items():
        match = re.match("(.*?)[(.*?)+]", v)
        if match:  #  Must be a Collection[] type
            collection, annotations = match.groups()
            print(annotations)
            ann = create_collection_annotation(
                k, collection, annotations.split(",")
            )
            anns.append(ann)
        else:
            anns.append(create_single_annotation(k, v))
    return anns


def create_module(classname: str, annotations: List[AnnAssign]) -> Module:
    """
    Boilerplate code to generate a class definition
    that inherits from TypedDict
    """
    classdef = ClassDef(
        name=classname,
        bases=[TypedDictBase],
        body=annotations,
        decorator_list=[],
    )
    module = Module(body=[classdef])
    return module


def create_typeddict(types: Dict[str, str]) -> str:
    """
    Create a pep8 typeddict string from the output of `reduce_types`
    """
    annotation = collect_annotations(types)
    module = create_module("Typed", annotation)
    code = astor.to_source(module)
    return code
