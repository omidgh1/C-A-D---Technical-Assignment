import pytest


def test_root_endpoint(client):
    """Test the root endpoint returns expected status and message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Carbon+Alt+Delete API is running"}


def test_create_measurement(client, auth_headers):
    response = client.post(
        "/measurements/",
        headers=auth_headers,
        json={"co2_value": 450.5, "unit": "ppm", "source": "unknown", "description": "test"}
    )
    assert response.status_code == 200
    assert response.json()["co2_value"] == 450.5


def test_get_all_measurements(client, auth_headers):
    client.post("/measurements/", headers=auth_headers,
                json={"co2_value": 400.0, "unit": "ppm", "source": "s1", "description": "test"})
    client.post("/measurements/", headers=auth_headers,
                json={"co2_value": 420.0, "unit": "ppm", "source": "s2", "description": "test"})

    response = client.get("/measurements/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_measurements_by_source(client, auth_headers):
    client.post("/measurements/", headers=auth_headers,
                json={"co2_value": 400.0, "unit": "ppm", "source": "s1", "description": "test"})
    client.post("/measurements/", headers=auth_headers,
                json={"co2_value": 420.0, "unit": "ppm", "source": "s2", "description": "test"})

    response = client.get("/measurements/?source=s2", headers=auth_headers)
    assert response.status_code == 200
    assert all(item["source"] == "s2" for item in response.json())


def test_get_single_measurement(client, auth_headers):
    post = client.post("/measurements/", headers=auth_headers,
                       json={"co2_value": 400.0, "unit": "ppm", "source": "s1", "description": "test"})
    id = post.json()["id"]

    response = client.get(f"/measurements/{id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == id


def test_update_measurement(client, auth_headers):
    post = client.post("/measurements/", headers=auth_headers,
                       json={"co2_value": 400.0, "unit": "ppm", "source": "s1", "description": "test"})
    id = post.json()["id"]

    response = client.put(f"/measurements/{id}", headers=auth_headers, json={"co2_value": 460.0})
    assert response.status_code == 200
    assert response.json()["co2_value"] == 460.0


def test_delete_measurement(client, auth_headers):
    post = client.post("/measurements/", headers=auth_headers,
                       json={"co2_value": 400.0, "unit": "ppm", "source": "s1", "description": "test"})
    id = post.json()["id"]

    response = client.delete(f"/measurements/{id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/measurements/{id}", headers=auth_headers)
    assert response.status_code == 404


def test_not_found(client, auth_headers):
    response = client.get("/measurements/999", headers=auth_headers)
    assert response.status_code == 404

    response = client.put("/measurements/999", headers=auth_headers, json={"co2_value": 500})
    assert response.status_code == 404

    response = client.delete("/measurements/999", headers=auth_headers)
    assert response.status_code == 404


def test_unauthorized_access(client):
    response = client.get("/measurements/")
    assert response.status_code == 401
