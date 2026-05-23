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
    # The 'start' command handles spawning new, detached windows reliably.
    django_cmd = f'start "Django Server" cmd /c "chcp 65001 >nul && call "{venv_activate}" && cd /d "{backend_dir}" && python manage.py runserver"'
    subprocess.Popen(django_cmd, env=current_env, shell=True)

    print("Starting Stripe Webhook Listener...")
    stripe_cmd = f'start "Stripe Webhook" cmd /c "echo Ensuing Stripe CLI connection... && stripe listen --forward-to http://localhost:8000/api/bookings/webhook/stripe/"'
    subprocess.Popen(stripe_cmd, env=current_env, shell=True)

    print("Launching PostgreSQL Unified Performance Monitor...")
    psql_path = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
    
    # We must construct a command that launches cmd, sets the title, and then runs psql, all in a new window.
    # To handle the \watch command without complicated escaping, we can write the query to a temporary SQL file
    # and have psql execute that file using the -f flag. This is the most robust method for complex queries and meta-commands.
    temp_sql_path = os.path.join(base_dir, "temp_monitor_query.sql")
    query_script = """
SELECT (SELECT now() - pg_postmaster_start_time()) AS uptime, 
       (SELECT count(*) FROM pg_stat_activity) AS active_conns, 
       (SELECT current_setting('max_connections')::int) AS max_conns, 
       (SELECT LEFT(query, 50) FROM pg_stat_activity WHERE state != 'idle' ORDER BY (now() - query_start) DESC LIMIT 1) AS longest_active_query, 
       (SELECT max(now() - query_start) FROM pg_stat_activity WHERE state != 'idle') AS max_query_duration, 
       (SELECT pg_size_pretty(sum(pg_database_size(datname))) FROM pg_database) AS total_disk_size, 
       (SELECT round(100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read) + 1), 2) FROM pg_stat_database) AS global_cache_hit_ratio \\watch 2
"""
    try:
        with open(temp_sql_path, "w", encoding="utf-8") as f:
            f.write(query_script.strip())
    except Exception as e:
        print(f"[ERROR] Could not create temp SQL file for monitor: {e}")
        input("Press Enter to continue...")
        sys.exit(1)

    # Launch psql using the temporary file in a new window
    # We add a pause at the end so if it fails immediately, the window doesn't close instantly before the user can read the error.
    psql_cmd = f'start "PostgreSQL Unified Performance Monitor" cmd /c ""{psql_path}" -U postgres -d postgres -f "{temp_sql_path}" || pause"'
    subprocess.Popen(psql_cmd, env=current_env, shell=True)

    print("\n-------------------------------------------------------")
    print("[SUCCESS] All 3 background workers deployed in separate windows!")
    print("You can safely close this terminal window.")
    print("-------------------------------------------------------\n")
    
    # Optional: clean up the temporary file after a short delay to ensure psql has time to open it.
    time.sleep(2)
    try:
         if os.path.exists(temp_sql_path):
             os.remove(temp_sql_path)
    except:
         pass
         
    sys.exit(0)

if __name__ == "__main__":
    main()
