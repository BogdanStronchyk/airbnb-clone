import os
import subprocess
import sys
import time

def main():
    print("=======================================================")
    print("   Initializing Secure Dev Stack (Django + Stripe + Postgres)")
    print("=======================================================\n")

    env_path = r"D:\env_storage\keys.env"
    env_vars = {}

    print("Loading configuration from hidden external .env...")
    if not os.path.exists(env_path):
        print(f"[ERROR] No secure .env file found at: {env_path}")
        print("Please check the path inside this script and try again.\n")
        input("Press Enter to continue...")
        sys.exit(1)

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    val = val.strip().strip('"').strip("'")
                    env_vars[key.strip()] = val
    except Exception as e:
        print(f"[ERROR] Failed to read .env file: {e}")
        input("Press Enter to continue...")
        sys.exit(1)

    if 'DATABASE_PASSWORD' not in env_vars:
        print("[ERROR] DATABASE_PASSWORD key was not found inside your external .env file!\n")
        input("Press Enter to continue...")
        sys.exit(1)

    # Prepare environment for child processes
    current_env = os.environ.copy()
    current_env.update(env_vars)
    current_env['PGPASSWORD'] = env_vars['DATABASE_PASSWORD']
    current_env['PGCLIENTENCODING'] = 'UTF8'
    current_env['PYTHONIOENCODING'] = 'utf-8'

    print("[SUCCESS] Vault unlocked. Environment variables mapped to memory.\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_activate = os.path.join(base_dir, ".venv", "Scripts", "activate.bat")
    backend_dir = os.path.join(base_dir, "backend")

    print("Starting Django Development Server...")
    # Use start /B to run in background or open new window. The bat used start "Django Server" cmd /c ...
    django_cmd = f'start "Django Server" cmd /c "chcp 65001 >nul && call "{venv_activate}" && cd /d "{backend_dir}" && python manage.py runserver"'
    subprocess.Popen(django_cmd, env=current_env, shell=True)

    print("Starting Stripe Webhook Listener...")
    stripe_cmd = f'start "Stripe Webhook" cmd /c "echo Ensuing Stripe CLI connection... && stripe listen --forward-to http://localhost:8000/api/bookings/webhook/stripe/"'
    subprocess.Popen(stripe_cmd, env=current_env, shell=True)

    print("\n-------------------------------------------------------")
    print("[SUCCESS] Background workers deployed!")
    print("This window will now act as your Live Database Monitor.")
    print("-------------------------------------------------------\n")
    
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=======================================================")
    print("   Launching PostgreSQL Unified Performance Monitor    ")
    print("=======================================================\n")

    psql_path = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
    query = "SELECT (SELECT now() - pg_postmaster_start_time()) AS uptime, (SELECT count(*) FROM pg_stat_activity) AS active_conns, (SELECT current_setting('max_connections')::int) AS max_conns, (SELECT LEFT(query, 50) FROM pg_stat_activity WHERE state != 'idle' ORDER BY (now() - query_start) DESC LIMIT 1) AS longest_active_query, (SELECT max(now() - query_start) FROM pg_stat_activity WHERE state != 'idle') AS max_query_duration, (SELECT pg_size_pretty(sum(pg_database_size(datname))) FROM pg_database) AS total_disk_size, (SELECT round(100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read) + 1), 2) FROM pg_stat_database) AS global_cache_hit_ratio \\watch 2"
    
    # Run psql in the current window using the secure environment variables
    subprocess.run([psql_path, '-U', 'postgres', '-d', 'postgres', '-c', query], env=current_env)

if __name__ == "__main__":
    main()
