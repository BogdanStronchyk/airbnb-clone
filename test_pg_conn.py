import psycopg2
import os

env_path = r"D:\env_storage\keys.env"
password = None

with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('DATABASE_PASSWORD'):
            password = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

if not password:
    print("Could not find password in keys.env")
    exit(1)

print(f"Attempting to connect with password of length: {len(password)}")

try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password=password, host='localhost', port='5432')
    print("CONNECTION SUCCESSFUL!")
    conn.close()
except Exception as e:
    print(f"CONNECTION FAILED: {e}")
