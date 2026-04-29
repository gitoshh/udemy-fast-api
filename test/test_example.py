def test_eq():
    assert 1 == 1

def test_ne():
    assert 1 != 2

def test_ty():
    assert type("Hello" is str)

def test_list():
    list_items = [1, 2, 3]
    assert type(list_items) is list
    assert 1 in list_items
    assert all([x > 0 for x in list_items])
    assert any([x > 2 for x in list_items])
