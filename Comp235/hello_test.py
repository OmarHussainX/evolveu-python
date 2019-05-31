from flask import json
import pytest
import hello


@pytest.fixture
def client():
    hello.app.config['TESTING'] = True
    client = hello.app.test_client()
    yield client


def test_root(client, capsys):
    rv = client.get('/')
    with capsys.disabled():
        print(f'\n ============= beginning test_root =============')
        print(f'\n --> response value: {rv}')
        print(f'\n --> headers: {rv.headers}')
        print(f'\n --> status, status code: {rv.status}, {rv.status_code}')
        print(f'\n --> data: {rv.data}')
        # assert(b'Larry' in rv.data)
        # assert(b'EvolveU Evaluation' in rv.data)
        print(f'\n ============== ending test_root ==============')


def test_info(client, capsys):
    rv = client.get('/info')
    data = json.loads(rv.data)
    with capsys.disabled():
        print(f'\n ============= beginning test_info =============')
        print(f'\n --> response value: {rv}')
        print(f'\n --> headers: {rv.headers}')
        print(f'\n --> status, status code: {rv.status}, {rv.status_code}')
        print(f'\n --> rv.data: {rv.data}')
        print(f'\n --> data: {data}')
        
        # https://wiki.python.org/moin/BytesStr
        # assert that the 'bytes' Object contains these bytes...
        assert(b'Rick' in rv.data)
        assert(b'Justin' in rv.data)
        
        assert('5' in data)
        print(f'\n ============== ending test_info ==============')
