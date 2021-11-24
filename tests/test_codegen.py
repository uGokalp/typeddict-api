from ast import AnnAssign

from src.codegen import (
    collect_annotations,
    collect_types,
    create_collection_annotation,
    create_single_annotation,
    create_typeddict,
    reduce_types,
)
from src.models import DictCode


def test_collect_types():
    dict_str = "{'a': 5}"
    code = DictCode(code=dict_str)
    types = collect_types(code.data)
    assert isinstance(types, dict)
    assert "a" in types.keys()
    assert {type(5)} in types.values()


def test_reduce_types():
    dict_str = "{'a': 5}"
    code = DictCode(code=dict_str)
    types = collect_types(code.data)
    reduced = reduce_types(types)
    assert isinstance(reduced, dict)


def test_collect_annotation():
    dict_str = "{'a': 5}"
    code = DictCode(code=dict_str)
    types = collect_types(code.data)
    reduced = reduce_types(types)
    annotations = collect_annotations(reduced)
    assert annotations is not None


def test_typeddict():
    dict_str = "{'a': 5}"
    code = DictCode(code=dict_str)
    types = collect_types(code.data)
    reduced = reduce_types(types)
    typed = create_typeddict(reduced)
    assert isinstance(typed, str)


def test_single_annotation():
    ann = create_single_annotation("a", int)
    assert isinstance(ann, AnnAssign)


def test_collection_annotation():
    ann = create_collection_annotation("a", "Union", [int, bool])
    assert isinstance(ann, AnnAssign)
