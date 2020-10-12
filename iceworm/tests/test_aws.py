from omnibus.docker.dev.pytest import DockerManager
from omnibus.inject.dev import pytest as ptinj
import boto3
import botocore.client


def test_docker_s3(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('minio', 9000)]).values()

    env = harness[DockerManager].compose_config['minio']['environment']
    cfg = {k: env['MINIO_' + k.upper()] for k in ['access_key', 'secret_key']}

    s3 = boto3.client(
        's3',
        endpoint_url=f'http://{host}:{port}',
        aws_access_key_id=cfg['access_key'],
        aws_secret_access_key=cfg['secret_key'],
        config=botocore.client.Config(signature_version='s3v4'),
        region_name='us-east-1',
    )

    bucket = 'abucket'
    try:
        s3.head_bucket(Bucket=bucket)
    except botocore.client.ClientError:
        s3.create_bucket(Bucket=bucket)
    s3.put_object(Bucket=bucket, Key='afile', Body=b'hi')
    print(s3.get_object(Bucket=bucket, Key='afile')['Body'].read())
