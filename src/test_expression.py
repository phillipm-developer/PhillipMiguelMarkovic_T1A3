from expression import Expression

import pytest

def test_parse_expression():
    pass

def test_is_float():
    # e = exp("x+1")
    assert Expression().is_float('12') == True
    assert exp.is_float('12.0') == True
    # assert exp.is_float('12.05') == True
    # assert exp.is_float('-12') == True
    # assert exp.is_float('-12.0') == True
    # assert exp.is_float('-12.55') == True
    # assert exp.is_float('0') == True
    # assert exp.is_float('0.0') == True
    # assert exp.is_float('-0') == True
    # assert exp.is_float('-0.0') == True
    # assert exp.is_float('twelve') == False
    # assert exp.is_float('100F') == False


def text_extract_variable_names():
    pass

def test_evaluate_list_of_values():
    pass

def test_evaluate_calc_dict():
    pass

def test_evaluate():
    pass

def test_assign_infix_list():
    pass

def test_check_syntax():
    pass

def test_assign_postfix_list():
    pass

def test_precedence_level():
    pass

def test_get_infix_list():
    pass

def test_get_postfix_list():
    pass

def test_is_operator():
    pass

def test_is_unary_operator():
    pass

def test_is_binary_operator():
    pass

def test_is_number_or_variable():
    pass

def test_remove_whitespace():
    pass


