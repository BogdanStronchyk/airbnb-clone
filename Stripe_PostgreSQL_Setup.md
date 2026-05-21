## Stripe CLI Installation and Setup

### 1. Install the Stripe CLI

**On macOS (using Homebrew):**
```bash
brew install stripe/stripe-cli/stripe
```

**On Windows (using Chocolatey):**
```bash
choco install stripe-cli
```

**On Linux (Debian/Ubuntu):**
```bash
curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
curl -sL https://raw.githubusercontent.com/stripe/stripe-cli/master/install.sh | sh
```

For other operating systems or detailed instructions, refer to the [official Stripe CLI documentation](https://stripe.com/docs/stripe-cli).

### 2. Configure the Stripe CLI

After installation, you need to link the CLI to your Stripe account. This will open a browser window for authentication.

```bash
stripe login
```

### 3. Forward Stripe Webhooks Locally

Once logged in, you can forward Stripe webhooks to your local Django development server. Replace `http://localhost:8000/api/bookings/webhook/stripe/` with the actual URL of your webhook endpoint if it's different.

```bash
stripe listen --forward-to http://localhost:8000/api/bookings/webhook/stripe/
```

This command will output a `whsec_` secret. **You need to add this secret to your Django project's `settings.py` or `keys.env` file as `STRIPE_WEBHOOK_SECRET`**.

## PostgreSQL Installation and Setup

### 1. Install PostgreSQL

**On macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**On Windows:**
Download the installer from the [official PostgreSQL website](https://www.postgresql.org/download/windows/) and follow the installation wizard. Remember the password you set for the `postgres` superuser.

**On Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create a PostgreSQL User and Database

After installation, you need to create a dedicated user and database for your Django project.

**On macOS/Linux:**
```bash
sudo -u postgres psql
```
Then, within the `psql` prompt, run:
```sql
CREATE USER airbnbuser WITH PASSWORD 'your_secure_password';
CREATE DATABASE airbnbdb OWNER airbnbuser;
\q
```
*Replace `airbnbuser`, `your_secure_password`, and `airbnbdb` with your desired username, password, and database name.*

**On Windows (using `psql` via Command Prompt):**
Open the SQL Shell (psql) from your PostgreSQL installation directory. Connect as the `postgres` user with the password you set during installation.

Then, within the `psql` prompt, run:
```sql
CREATE USER airbnbuser WITH PASSWORD 'your_secure_password';
CREATE DATABASE airbnbdb OWNER airbnbuser;
\q
```

### 3. Configure Django to Use PostgreSQL

Update your `backend/core/settings.py` file to use the new PostgreSQL database. You'll need to install `psycopg2` first:

```bash
pip install psycopg2-binary
```

Then, modify your `DATABASES` setting in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'airbnbdb',        # Your database name
        'USER': 'airbnbuser',      # Your database user
        'PASSWORD': 'your_secure_password', # Your database password
        'HOST': 'localhost',
        'PORT': '',                # Default PostgreSQL port is 5432
    }
}
```

Replace `'airbnbdb'`, `'airbnbuser'`, and `'your_secure_password'` with the values you set in Step 2. If you're running PostgreSQL on a non-standard port, update the `'PORT'` value.

### 4. Apply Migrations

After configuring Django, apply the database migrations:

```bash
python manage.py migrate
```

This will set up your database schema.