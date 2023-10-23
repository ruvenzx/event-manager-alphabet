from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post(
        "/event",
        json={"title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }
    return response["id"]

id = test_create_item()

def test_read_item(id):
    response = client.get(f"/event/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id
    
def test_read_all_items():
    response = client.get("/event")
    assert response.status_code == 200

def test_read_inexistent_item():
    response = client.get("/event/-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    
def test_update_item(id):
    response = client.put(f"/event/{id}", json={})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }
    
def test_delete_item(id):
    response = client.delete(f"/event/{id}")
    assert response.status_code == 200