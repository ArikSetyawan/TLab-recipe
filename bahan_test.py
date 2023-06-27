def test_get_all_bahan(client):
    res = client.get('/api/bahan')
    assert res.status_code == 200

def test_get_bahan_by_id(client):
    res = client.get('/api/bahan?id_bahan=1')
    assert res.status_code == 200

def test_get_bahan_by_id_not_found(client):
    res = client.get('/api/bahan?id_bahan=100')
    assert res.status_code == 404

def test_create_bahan(client):
    res = client.post('/api/bahan', json={'name': 'Bahan Test'})
    assert res.status_code == 200