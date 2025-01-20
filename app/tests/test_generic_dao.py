from app.dao.generic_dao import BaseDAO

def test_generic_insert():
    dao = BaseDAO()
    insert_data = {"name": "Item 1", "description": "Description 1"}
    new_id = dao.generic_insert(insert_data)
    result = dao.generic_get_by_field("id", new_id)
    assert result[1] == "Item 1"
    assert result[2] == "Description 1"
    #ADD second item
    insert_data = {"name": "Item 2", "description": "Description 2"}
    new_id = dao.generic_insert(insert_data)
    result = dao.generic_get_by_field("id", new_id)
    assert result[1] == "Item 2"

def test_generic_search_exact_match():
    dao = BaseDAO()
    search_data = {"name": "Item 1"}
    result = dao.generic_search(search_data)
    assert result[0][1] == "Item 1"

def test_generic_search_like_match():
    dao = BaseDAO()
    search_data = {"name": "Item"}
    result = dao.generic_search(search_data, like=True)
    assert len(result) == 2

def test_generic_search_multiple_conditions():
    dao = BaseDAO()
    search_data = {"name": "Item 1", "description": "Description 1"}
    result = dao.generic_search(search_data)
    assert len(result) == 1
    assert result[0][1] == "Item 1"
    assert result[0][2] == "Description 1"

def test_generic_get_all():
    dao = BaseDAO()
    result = dao.generic_get_all()
    assert len(result) == 2

def test_generic_get_by_field_exact_match():
    dao = BaseDAO()
    result = dao.generic_get_by_field("name", "Item 1")
    assert result[1] == "Item 1"

def test_generic_update():
    dao = BaseDAO()
    update_data = {"id": 1, "name": "Updated Item 1", "description": "Updated Description 1"}
    rows_affected = dao.generic_update("id", update_data)
    result = dao.generic_get_by_field("id", 1)
    assert rows_affected == 1
    assert result[1] == "Updated Item 1"
    assert result[2] == "Updated Description 1"

def test_generic_replace():
    dao = BaseDAO()
    replace_data = {"id": 1, "name": "Replaced Item 1", "description": "Replaced Description 1"}
    rows_affected = dao.generic_replace(replace_data)
    result = dao.generic_get_by_field("id", 1)
    assert rows_affected == 1
    assert result[1] == "Replaced Item 1"
    assert result[2] == "Replaced Description 1"

def test_generic_delete():
    dao = BaseDAO()
    rows_affected = dao.generic_delete("id", 1)
    assert rows_affected == 1