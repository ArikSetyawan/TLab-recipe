def test_get_all_kategori(client):
    response = client.get('/api/kategori')
    assert response.status_code == 200

def test_get_kategori_by_id(client):
    response = client.get('/api/kategori?id_kategori=1')
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data']['id'] == 1

def test_get_kategori_by_id_not_found(client):
    expected_error = {
        "success": False,
        "message": "Kategori Not Found",
        "data": None,
        "error": None
    }
    response = client.get('/api/kategori?id_kategori=100')
    assert response.status_code == 404
    assert response.json == expected_error

def test_create_kategori(client):
    # Crete Kategori
    res = client.post('/api/kategori', json={'name': 'Kategori Test Create'})
    response_json  = res.json

    assert res.status_code == 201
    assert response_json['success'] == True
    assert response_json['data']['name'] == 'Kategori Test Create'

    # delete kategori
    res_delete = client.delete('/api/kategori', json={'id_kategori': response_json['data']['id']})
    assert res_delete.status_code == 200

def test_update_kategori(client):
    # create kategori for update
    payload = {'name': 'Kategori Test Update'}
    res_create = client.post('/api/kategori', json=payload)
    assert res_create.status_code == 201

    id_kategori = res_create.json['data']['id']

    # Change Payload name value
    payload['name'] = "Kategori Test Update 2"
    # add id to payload
    payload['id_kategori'] = id_kategori

    # update kategori
    response_update = client.put('/api/kategori', json=payload)
    response_json  = response_update.json

    assert response_update.status_code == 200
    assert response_json['success'] == True
    assert response_json['data']['name'] == 'Kategori Test Update 2'

    # delete kategori
    res_delete = client.delete('/api/kategori', json={'id_kategori': id_kategori})
    assert res_delete.status_code == 200

def test_delete_kategori(client):
    # create kategori for delete
    payload = {'name': 'Kategori Test Delete'}
    res_create = client.post('/api/kategori', json=payload)
    assert res_create.status_code == 201

    id_kategori = res_create.json['data']['id']

    # delete kategori
    res = client.delete('/api/kategori', json={'id_kategori': id_kategori})
    response_json  = res.json

    assert res.status_code == 200
    assert response_json['success'] == True