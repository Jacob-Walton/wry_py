import pytest
import wry_py


def test_sum_as_string():
    assert wry_py.sum_as_string(1, 1) == "2"
