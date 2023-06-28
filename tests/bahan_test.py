def test_get_all_bahan(client):
    res = client.get('/api/bahan')
    assert res.status_code == 200

def test_get_bahan_by_id(client):
    res = client.get('/api/bahan?id_bahan=1')
    response_json  = res.json
    assert res.status_code == 200
    assert response_json['success'] == True
    assert response_json['data']['id'] == 1

def test_get_bahan_by_id_not_found(client):
    expected_error = {
        "success": False,
        "message": "Bahan Not Found",
        "data": None,
        "error": None
    }
    res = client.get('/api/bahan?id_bahan=100')
    assert res.status_code == 404
    assert res.json == expected_error

def test_create_bahan(client):
    # Crete bahan
    res = client.post('/api/bahan', json={'name': 'Bahan Test Create'})
    response_json  = res.json

    assert res.status_code == 201
    assert response_json['success'] == True
    assert response_json['data']['name'] == 'Bahan Test Create'

    # delete bahan
    res_delete = client.delete('/api/bahan', json={'id_bahan': response_json['data']['id']})
    assert res_delete.status_code == 200

def test_update_bahan(client):
    # create bahan for update
    payload = {'name': 'Bahan Test Update'}
    res_create = client.post('/api/bahan', json=payload)
    assert res_create.status_code == 201

    id_bahan = res_create.json['data']['id']

    # Change Payload name value
    payload['name'] = "Bahan Test Update 2"
    # add id to payload
    payload['id_bahan'] = id_bahan

    # update bahan
    response_update = client.put('/api/bahan', json=payload)
    response_json  = response_update.json

    assert response_update.status_code == 200
    assert response_json['success'] == True
    assert response_json['data']['name'] == 'Bahan Test Update 2'

    # delete bahan
    res_delete = client.delete('/api/bahan', json={'id_bahan': id_bahan})
    assert res_delete.status_code == 200

def test_delete_bahan(client):
    # create bahan for delete
    payload = {'name': 'Bahan Test Delete'}
    res_create = client.post('/api/bahan', json=payload)
    assert res_create.status_code == 201

    id_bahan = res_create.json['data']['id']

    # delete bahan
    res = client.delete('/api/bahan', json={'id_bahan': id_bahan})
    response_json  = res.json

    assert res.status_code == 200
    assert response_json['success'] == True