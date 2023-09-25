# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

# This script retrieves Aurora database user credential in AWS Secrets Manager and connect aurora using the credential.
import boto3
import json
import pymysql

from botocore.exceptions import ClientError

host = "mydatabaseinstanceendpointhere"
port = 3306
database = "mysql"
username = "demouser"
password = "password" # dummy value for now
versionstages = ""

def get_secret():

    secret_name = "secretnamehere"
    region_name = "ap-northeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])
    version_stages = get_secret_value_response['VersionStages']

    return secret, version_stages

# Your code goes here.
secret, versionstages = get_secret()

username = secret['username']
host = secret['host']
password = secret['password']
port = secret['port']

print (username, host, port, password)
print (versionstages)

conn = pymysql.connect(host=host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
cursor = conn.cursor()

query = "show tables like 'user'"
res = cursor.execute(query)
print (res)
conn.close()




