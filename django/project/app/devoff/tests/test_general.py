import random

import factory
from rest_framework.reverse import reverse


def test_general():
    assert True


def test_encrypt_fail(client):
    """Tests that 'mensaje' and 'vueltas' are required."""
    response = client.post(reverse("devoff:encrypt"), content_type="application/json",)
    assert response.status_code == 422
    assert "mensaje" in response.json()
    assert "vueltas" in response.json()


def test_encrypt_vuelta_type(client):
    """Tests that 'vueltas' can't be a string."""

    mensaje = factory.Faker("word").generate()
    vueltas = factory.Faker("word").generate()
    body = {"mensaje": mensaje, "vueltas": vueltas}
    response = client.post(
        reverse("devoff:encrypt"), data=body, content_type="application/json",
    )
    assert response.status_code == 422
    assert "vueltas" in response.json()
    assert response.json()["vueltas"] == ["A valid integer is required."]


def test_encrypt(client):
    """Test that some example encrypt works."""
    body = {"mensaje": "Devoff se puso ATR", "vueltas": 4}
    response = client.post(
        reverse("devoff:encrypt"), data=body, content_type="application/json",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "mensaje" in response_json
    assert response_json["mensaje"] == "DfesTef oRv p osuA"


def test_encrypt_2(client):
    """Test that some example encrypt works."""
    body = {"mensaje": "Devoff se puso ATR!.", "vueltas": 4}
    response = client.post(
        reverse("devoff:encrypt"), data=body, content_type="application/json",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "mensaje" in response_json
    assert response_json["mensaje"] == "DfesTef oRv p !osuA."


def test_decrypt(client):
    """Test that some example decrypt works."""
    body = {"mensaje": "DfesTef oRv p osuA", "vueltas": 4}
    response = client.post(
        reverse("devoff:decrypt"), data=body, content_type="application/json",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "mensaje" in response_json
    assert response_json["mensaje"] == "Devoff se puso ATR"


def test_decrypt_2(client):
    """Test that some example decrypt works."""
    body = {"mensaje": "DfesTef oRv p !osuA.", "vueltas": 4}
    response = client.post(
        reverse("devoff:decrypt"), data=body, content_type="application/json",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "mensaje" in response_json
    assert response_json["mensaje"] == "Devoff se puso ATR!."
