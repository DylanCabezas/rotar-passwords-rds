import boto3
import pymysql
import os
import random
import string
import json

def generar_password(longitud=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(longitud))

def lambda_handler(event, context):
    # Lista de stages y sus respectivos usuarios
    stages = {
        'dev': 'user_dev',
        'test': 'user_test',
        'prod': 'user_prod'
    }

    admin_user = 'admin'
    ssm = boto3.client('ssm')
    secretsmanager = boto3.client('secretsmanager')

    # Obtener la contraseña del usuario admin desde Parameter Store
    response = ssm.get_parameter(
        Name='/rds_mysql_alumnos/admin/password',
        WithDecryption=True
    )
    admin_password = response['Parameter']['Value']

    # Obtener host de la base de datos desde Secrets Manager (uno solo para todos los stages)
    secret_sample = secretsmanager.get_secret_value(SecretId='dev/alumnos')
    db_host = json.loads(secret_sample['SecretString'])['host']

    resultados = {}

    for stage, usuario in stages.items():
        nuevo_password = generar_password()

        try:
            # Conectarse a la base con usuario admin
            connection = pymysql.connect(
                host=db_host,
                user=admin_user,
                password=admin_password,
                db=stage,
                connect_timeout=5
            )

            with connection.cursor() as cursor:
                cursor.execute(f"ALTER USER '{usuario}'@'%' IDENTIFIED BY '{nuevo_password}';")
                connection.commit()

            connection.close()

            # Actualizar en Parameter Store
            ssm.put_parameter(
                Name=f"/rds_mysql_alumnos/{usuario}/password",
                Value=nuevo_password,
                Type='SecureString',
                Overwrite=True
            )

            # Actualizar en Secrets Manager
            secret_id = f"{stage}/alumnos"
            secret_value = secretsmanager.get_secret_value(SecretId=secret_id)
            parsed_secret = json.loads(secret_value['SecretString'])
            parsed_secret['password'] = nuevo_password

            secretsmanager.update_secret(
                SecretId=secret_id,
                SecretString=json.dumps(parsed_secret)
            )

            resultados[stage] = "Password rotado exitosamente"

        except Exception as e:
            resultados[stage] = f"Error: {str(e)}"

    return {
        "statusCode": 200,
        "body": json.dumps(resultados)
    }
