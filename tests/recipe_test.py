def test_get_all_recipe(client):
    response = client.get("/api/recipe")
    assert response.status_code == 200

def test_get_recipe_by_id(client):
    response = client.get("/api/recipe?id_recipe=1")
    assert response.status_code == 200

def test_get_recipe_by_id_kategori(client):
    response = client.get("/api/recipe?id_kategori=1")
    assert response.status_code == 200

def test_get_recipe_by_id_bahan(client):
    response = client.get("/api/recipe?id_bahan=1")
    assert response.status_code == 200

def test_get_recipe_by_id_bahan_and_kategori(client):
    response = client.get("/api/recipe?id_bahan=1&id_kategori=1")
    assert response.status_code == 200

def test_create_recipe(client):
    # Create Kategori for new Recipe
    response_kategori = client.post("/api/kategori", json={'name':'Main Course New Recipe'})
    assert response_kategori.status_code == 201

    id_kategori = response_kategori.json['data']['id']

    # create Bahan for new Recipe
    response_bahan1 = client.post("/api/bahan", json={'name':'Bahan New Recipe'})
    assert response_bahan1.status_code == 201

    response_bahan2 = client.post("/api/bahan", json={'name':'Bahan New Recipe 2'})
    assert response_bahan2.status_code == 201

    id_bahan1 = response_bahan1.json['data']['id']
    id_bahan2 = response_bahan2.json['data']['id']

    # define payload for new Recipe
    payload = {
        "name": "Nasi Goreng",
        "description": "Nasi Goreng Mawut",
        "id_kategori": id_kategori,
        "ingredients":[{'id_bahan':id_bahan1,'quantity':'1','satuan':'Secukupnya'},{'id_bahan':id_bahan2,'satuan':'Secukupnya'}]
    }

    # create new Recipe
    response_new_recipe = client.post("/api/recipe", json=payload)
    assert response_new_recipe.status_code == 201

    # remove recipe
    response_remove_recipe = client.delete("/api/recipe", json={'id_recipe':response_new_recipe.json['data']['id']})
    assert response_remove_recipe.status_code == 200

    # remove kategori
    response_remove_kategori = client.delete("/api/kategori", json={'id_kategori':id_kategori})
    assert response_remove_kategori.status_code == 200

    # remove id_bahan1
    response_remove_bahan1 = client.delete("/api/bahan", json={'id_bahan':id_bahan1})
    assert response_remove_bahan1.status_code == 200

    # remove id_bahan2
    response_remove_bahan2 = client.delete("/api/bahan", json={'id_bahan':id_bahan2})
    assert response_remove_bahan2.status_code == 200