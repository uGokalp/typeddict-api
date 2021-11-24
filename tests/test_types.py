from random import randint

from src.ordered_set import OrderedSet


def test_set_init_five():
    oset = OrderedSet([5])
    assert 5 in oset


def test_set_add_five():
    oset = OrderedSet([])
    oset.add(5)
    assert 5 in oset


def test_set_add_random():
    num = randint(0, 1000)
    oset = OrderedSet([])
    oset.add(num)
    assert num in oset


def test_set_discard_random():
    num = randint(0, 1000)
    oset = OrderedSet([num])
    assert num in oset
    oset.discard(num)
    assert num not in oset


def test_set_is_list():
    num = randint(0, 1000)
    oset = OrderedSet([num])
    assert isinstance(oset.data, list)
