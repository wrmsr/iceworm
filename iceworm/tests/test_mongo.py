from omnibus import docker
import pymongo
import pytest


@pytest.mark.xfail()
def test_docker_mongo():
    if docker.is_in_docker():
        (host, port) = 'iceworm-mongo', 27017

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_iceworm-mongo_1', 27017)])

        [(host, port)] = eps.values()

    client = pymongo.MongoClient(f'mongodb://root:iceworm@{host}:{port}')
    db = client['test-database']

    post = {
        'author': 'Mike',
        'text': 'My first blog post!',
        'tags': ['mongodb', 'python', 'pymongo'],
    }

    posts = db['posts']
    post_id = posts.insert_one(post).inserted_id
    print(post_id)
    db.list_collection_names()
    print(posts.find_one())
