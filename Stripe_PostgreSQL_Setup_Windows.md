## Stripe CLI Installation and Setup (Windows - No External Add-ons)

### 1. Install the Stripe CLI

**On Windows:**

1.  **Download the Stripe CLI:** Go to the [Stripe CLI releases page on GitHub](https://github.com/stripe/stripe-cli/releases). Look for the latest release and download the `.msi` installer for Windows (e.g., `stripe_1.x.x_windows_x86_64.msi`).
2.  **Run the Installer:** Double-click the downloaded `.msi` file and follow the on-screen instructions to install the Stripe CLI. This will add `stripe` to your system's PATH.
3.  **Verify Installation:** Open a new Command Prompt or PowerShell window and type:
    ```cmd
    stripe version
    ```
    You should see the installed version of the Stripe CLI.

### 2. Configure the Stripe CLI

After installation, you need to link the CLI to your Stripe account. This will open a browser window for authentication.

```cmd
stripe login
```

### 3. Forward Stripe Webhooks Locally

Once logged in, you can forward Stripe webhooks to your local Django development server. Replace `http://localhost:8000/api/bookings/webhook/stripe/` with the actual URL of your webhook endpoint if it's different.

```cmd
stripe listen --forward-to http://localhost:8000/api/bookings/webhook/stripe/
```

This command will output a `whsec_` secret. **You need to add this secret to your Django project's `settings.py` or `keys.env` file as `STRIPE_WEBHOOK_SECRET`**.

## PostgreSQL Installation and Setup (Windows - No External Add-ons)

### 1. Install PostgreSQL

**On Windows:**

1.  **Download the PostgreSQL Installer:** Go to the [official PostgreSQL website for Windows downloads](https://www.postgresql.org/download/windows/). Download the interactive installer by EnterpriseDB for your Windows version.
2.  **Run the Installer:** Double-click the downloaded executable and follow the installation wizard. 
    *   **Installation Directory:** You can accept the default or choose a different path.
    *   **Select Components:** You typically need `PostgreSQL Server`, `pgAdmin 4`, and `Command Line Tools`. Stack Builder is optional.
    *   **Data Directory:** Accept the default or choose a preferred location.
    *   **Password:** **Crucially, you will be asked to set a password for the `postgres` superuser.** Remember this password, as you'll need it to access PostgreSQL.
    *   **Port:** The default port is `5432`. You can usually leave this as default.
    *   **Locale:** Choose your preferred locale.
3.  **Complete Installation:** Finish the wizard. Stack Builder might launch, which you can use to install additional drivers/tools, but it's not strictly necessary for basic setup.

### 2. Create a PostgreSQL User and Database

Open the **SQL Shell (psql)** from your PostgreSQL installation directory (you can find it in your Start Menu under 'PostgreSQL 1X').

1.  **Connect to PostgreSQL:** When prompted for 'Server', 'Database', 'Port', 'Username', press Enter to accept the defaults (localhost, postgres, 5432, postgres). When prompted for 'Password', enter the `postgres` superuser password you set during installation.

2.  **Create User and Database:** Once connected, run the following SQL commands. Replace `your_django_user`, `your_secure_password`, and `your_django_db` with your desired username, password, and database name. Make sure to use a strong password.

    ```sql
    CREATE USER postgres WITH PASSWORD 'D3£1`(r2NGok';
    CREATE DATABASE airbnb_db OWNER postgres;
    \q
    ```

### 3. Configure Django to Use PostgreSQL

Update your `backend/core/settings.py` file to use the new PostgreSQL database. You'll need to install the `psycopg2` adapter first.

1.  **Install `psycopg2`:** Open a Command Prompt in your project's virtual environment and run:
    ```cmd
    pip install psycopg2-binary
    ```

2.  **Modify `settings.py`:** Update your `DATABASES` setting in `backend/core/settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_django_db',        # Your database name
            'USER': 'your_django_user',      # Your database user
            'PASSWORD': 'your_secure_password', # Your database password
            'HOST': 'localhost',
            'PORT': '',                # Default PostgreSQL port is 5432
        }
    }
    ```

    Replace `'your_django_db'`, `'your_django_user'`, and `'your_secure_password'` with the values you set in Step 2. If you're running PostgreSQL on a non-standard port, update the `'PORT'` value (e.g., `'5432'`).

### 4. Apply Migrations

After configuring Django, apply the database migrations:

```cmd
python manage.py migrate
```

This will set up your database schema.

### 5. Data Migration (Optional)

If you want to migrate data from an existing SQLite database (e.g., `db.sqlite3`):

1.  **Dump data from old database:** On your *old machine* (or where your SQLite database is), navigate to your Django project root and run:
    ```cmd
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > datadump.json
    ```
    This creates a `datadump.json` file with your application data.

2.  **Copy `datadump.json`:** Transfer the `datadump.json` file to the root of your Django project on the *new machine*.

3.  **Load data into new database:** On the *new machine*, in your project's virtual environment, run:
    ```cmd
    python manage.py loaddata datadump.json
    ```
    This will populate your new PostgreSQL database with your existing data.