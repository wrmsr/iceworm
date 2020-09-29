from omnibus.docker.dev.pytest import DockerManager
from omnibus.inject.dev.pytest import harness as har
import pymongo


def test_docker_mongo(harness: har.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('mongo', 27017)]).values()

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
