import os

class Config:
    # Mode: 'production' or 'development'
    # In development, we use local mock directories instead of /etc/apache2
    MODE = os.environ.get('APP_MODE', 'development')

    if MODE == 'production':
        APACHE_SITES_AVAILABLE = '/etc/apache2/sites-available'
        APACHE_SITES_ENABLED = '/etc/apache2/sites-enabled'
        APACHE_LOG_DIR = '/var/log/apache2'
        WEB_ROOT = '/var/www/html'
        RELOAD_CMD = 'sudo systemctl reload apache2'
        CERTBOT_CMD = 'sudo certbot --apache'
    else:
        # Mock paths for development/sandbox
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        MOCK_DIR = os.path.join(BASE_DIR, 'mock_fs')

        APACHE_SITES_AVAILABLE = os.path.join(MOCK_DIR, 'sites-available')
        APACHE_SITES_ENABLED = os.path.join(MOCK_DIR, 'sites-enabled')
        APACHE_LOG_DIR = os.path.join(MOCK_DIR, 'logs')
        WEB_ROOT = os.path.join(MOCK_DIR, 'www')

        # Mock commands
        RELOAD_CMD = 'echo "Simulating Apache Reload"'
        CERTBOT_CMD = 'echo "Simulating Certbot"'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Create mock directories if they don't exist in dev mode
if Config.MODE != 'production':
    os.makedirs(Config.APACHE_SITES_AVAILABLE, exist_ok=True)
    os.makedirs(Config.APACHE_SITES_ENABLED, exist_ok=True)
    os.makedirs(Config.APACHE_LOG_DIR, exist_ok=True)
    os.makedirs(Config.WEB_ROOT, exist_ok=True)
