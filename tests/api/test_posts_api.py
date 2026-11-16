"""
Pruebas de API sobre JSONPlaceholder (https://jsonplaceholder.typicode.com).

Nota: JSONPlaceholder es una API falsa. POST y DELETE responden como si
funcionaran, pero no guardan nada. Por eso el encadenamiento lo hago
con datos que sí existen (post -> autor -> comentarios).
"""
import pytest

from utils.helpers import read_json

pytestmark = pytest.mark.api

API_DATA = read_json("api_data.json")

# Estructura esperada de un post: campo -> tipo
POST_SCHEMA = {"userId": int, "id": int, "title": str, "body": str}


def assert_matches_schema(item, schema):
    for field, expected_type in schema.items():
        assert field in item, f"Falta el campo '{field}' en {item}"
        assert isinstance(item[field], expected_type), (
            f"'{field}' debería ser {expected_type.__name__} y es {type(item[field]).__name__}"
        )


# ---------- GET ----------

def test_get_post_by_id(api):
    response = api.get("/posts/1")

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    post = response.json()
    assert_matches_schema(post, POST_SCHEMA)
    assert post["id"] == 1


@pytest.mark.parametrize("user_id", API_DATA["user_ids"])
def test_get_posts_filtered_by_user(api, user_id):
    response = api.get("/posts", params={"userId": user_id})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0, f"El usuario {user_id} no tiene posts"
    assert all(post["userId"] == user_id for post in posts)


def test_get_nonexistent_post_returns_404(api):
    response = api.get("/posts/99999")

    assert response.status_code == 404
    assert response.json() == {}


# ---------- POST ----------

@pytest.mark.parametrize("new_post", API_DATA["new_posts"], ids=lambda p: p["case_id"])
def test_create_post(api, new_post):
    payload = {key: new_post[key] for key in ("title", "body", "userId")}
    response = api.post("/posts", payload)

    assert response.status_code == 201
    created = response.json()
    assert_matches_schema(created, POST_SCHEMA)
    # La API devuelve lo mismo que se mandó + el id nuevo
    for key, value in payload.items():
        assert created[key] == value


# ---------- DELETE ----------

def test_delete_post(api):
    response = api.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {}


# ---------- Encadenamiento ----------

def test_post_author_and_comments_chain(api):
    # 1. Traer un post
    post = api.get("/posts/3").json()
    author_id = post["userId"]

    # 2. Con el userId del post, traer al autor
    author_response = api.get(f"/users/{author_id}")
    assert author_response.status_code == 200
    author = author_response.json()
    assert author["id"] == author_id
    assert "@" in author["email"]

    # 3. Con el id del post, traer sus comentarios
    comments_response = api.get(f"/posts/{post['id']}/comments")
    assert comments_response.status_code == 200
    comments = comments_response.json()
    assert len(comments) > 0
    assert all(comment["postId"] == post["id"] for comment in comments)
