# 🔐 Rotación de Contraseñas MySQL con AWS Secrets Manager – Ejercicio 2

Este proyecto utiliza **AWS Secrets Manager** como herramienta principal para implementar la rotación automática de contraseñas en una base de datos MySQL alojada en Amazon RDS.  
La función Lambda se ejecuta automáticamente cada 10 minutos mediante **Amazon EventBridge** y actualiza los secretos tanto en **Secrets Manager** como en **Parameter Store**, cumpliendo los requisitos del **Ejercicio 2**.

---

## ✅ Objetivo del Ejercicio 2

> Implementar la **rotación de contraseñas** para los usuarios `user_dev`, `user_test` y `user_prod` de la base de datos RDS.  
> Actualizar las credenciales **tanto en Secrets Manager como en Systems Manager Parameter Store** usando un Lambda que se ejecute **cada 10 minutos con EventBridge**.  
> Además, almacenar en Parameter Store la clave del usuario `admin`.

---

## ⚙️ Tecnología utilizada

- AWS Lambda  
- AWS Secrets Manager ✅  
- AWS Systems Manager Parameter Store  
- Amazon RDS (MySQL)  
- Amazon EventBridge (programador)  
- Serverless Framework  
- Python 3.13  
- PyMySQL  

---

## 📁 Estructura del Proyecto

rotar-passwords-rds/

│

├── RotarPasswordUsuarios.py # Función Lambda que rota contraseñas

├── serverless.yml # Configuración de Lambda + EventBridge

├── requirements.txt # pymysql

└── pymysql/ # Librería instalada con pip install -t .

---

## 🪪 Parámetro previo requerido

```bash
aws ssm put-parameter \
  --name /rds_mysql_alumnos/admin/password \
  --value "MiClaveSegura123" \
  --type SecureString
```

🧪 Despliegue
```bash
pip install pymysql -t .
```

```bash
sls deploy
```

Para no esperar los 10 minutos se puede probar con este comando:
```bash
aws lambda invoke \
  --function-name rotar-passwords-rds-dev-rotar \
  response.json
cat response.json
```


Para ver el cambio de password:

AWS Secrets Manager -> Secretos -> dev/alumnos -> Descripción General -> Valor del Secreto
AWS Secrets Manager -> Secretos -> prod/alumnos -> Descripción General -> Valor del Secreto
AWS Secrets Manager -> Secretos -> test/alumnos -> Descripción General -> Valor del Secreto


🧑‍💻 Autor
Dylan Cabezas
CS2032
