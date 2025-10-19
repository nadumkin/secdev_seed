
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_should_not_allow_sql_injection():
    # Ожидаем, что вход с username, содержащим SQL-комментарий, должен БЫТЬ запрещён.
    payload = {"username": "admin'-- ", "password": "x"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 422, "SQLi-бэйпас логина должен быть закрыт"

def test_login_should_fail_if_username_is_invalid():
    payload = {"username": "a", "password": "validpass1"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 422, "Имя пользователя должно быть длиной от 3 символов"

def test_login_should_fail_if_password_is_invalid():
    payload = {"username": "validuser", "password": "short"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 422, "Пароль должен содержать хотя бы одну цифру и быть длиной от 6 символов"
