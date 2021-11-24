from src.validate import can_eval, can_parse, make_dict

int_example = '{"b": 1}'
int_set_example = '{"c": {1, 2}}'
str_set_example = '{"d" : {"1", "2"}}'
int_list_example = '{"e": [1,2]}'
int_bool_list_example = '{"f": [1, True]}'

invalid_dict = '{"b": 1'

basic_list = "[1, 2]"
basic_set = "{1, 2}"


def test_can_parse_int_dict():
    assert can_parse(int_example) is True


def test_cant_parse_invalid_dict():
    assert can_parse(invalid_dict) is False


def test_can_eval_types():
    assert can_eval(basic_list) is True
    assert can_eval(basic_set) is True


def test_can_make_dict():
    assert make_dict(int_example) == dict(b=1)
