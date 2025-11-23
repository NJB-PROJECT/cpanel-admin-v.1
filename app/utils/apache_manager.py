import os
import subprocess
import re
from app.config import Config

def is_valid_domain(domain_name):
    """
    Validates domain name format.
    Allows alphanumeric, hyphens, and dots.
    Strictly forbids slashes, spaces, or other special chars.
    """
    if not domain_name:
        return False
    # Regex for standard domain format (simplified)
    # ^[a-zA-Z0-9] starts with alphanumeric
    # [a-zA-Z0-9-\.]* follows
    # [a-zA-Z0-9]$ ends with alphanumeric
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-\.]{0,253}[a-zA-Z0-9])?$'
    if not re.match(pattern, domain_name):
        return False

    # extra safety: explicit check for path traversal attempts
    if '..' in domain_name or '/' in domain_name or '\\' in domain_name:
        return False

    return True

def list_domains():
    """
    Lists domains based on files in sites-available.
    Returns a list of dictionaries: {'domain': 'example.com', 'enabled': True/False, 'file': 'filename'}
    """
    domains = []
    if not os.path.exists(Config.APACHE_SITES_AVAILABLE):
        return []

    files = os.listdir(Config.APACHE_SITES_AVAILABLE)
    for f in files:
        if f.endswith('.conf') and f not in ['000-default.conf', 'default-ssl.conf']:
            domain_name = f.replace('.conf', '')
            is_enabled = os.path.exists(os.path.join(Config.APACHE_SITES_ENABLED, f))
            domains.append({
                'domain': domain_name,
                'file': f,
                'enabled': is_enabled
            })
    return domains

def create_domain(domain_name, email):
    """
    Creates a new Virtual Host configuration file.
    """
    if not is_valid_domain(domain_name):
        return False, "Invalid domain name format"

    # Minimal email validation
    if not email or '@' not in email:
        return False, "Invalid email address"

    conf_content = f"""<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain_name}
    ServerAlias www.{domain_name}
    DocumentRoot {Config.WEB_ROOT}/{domain_name}

    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined

    <Directory {Config.WEB_ROOT}/{domain_name}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""

    file_path = os.path.join(Config.APACHE_SITES_AVAILABLE, f"{domain_name}.conf")

    try:
        # Create Document Root
        doc_root = os.path.join(Config.WEB_ROOT, domain_name)
        # Using os.path.join with validated domain prevents traversal,
        # but abspath check is a good backup practice.
        if not os.path.abspath(doc_root).startswith(os.path.abspath(Config.WEB_ROOT)):
             return False, "Security Error: Path traversal detected"

        os.makedirs(doc_root, exist_ok=True)

        # Create index.html placeholder
        with open(os.path.join(doc_root, 'index.html'), 'w') as f:
            f.write(f"<h1>Welcome to {domain_name}!</h1><p>Hosted on Jarvis Clouding Control Panel</p>")

        # Write Config File
        with open(file_path, 'w') as f:
            f.write(conf_content)

        return True, "Domain created successfully"
    except Exception as e:
        return False, str(e)

def toggle_domain(domain_name, enable=True):
    """
    Enables (symlink) or disables (remove symlink) a site.
    """
    if not is_valid_domain(domain_name):
        return False, "Invalid domain name"

    conf_file = f"{domain_name}.conf"
    avail_path = os.path.join(Config.APACHE_SITES_AVAILABLE, conf_file)
    enabled_path = os.path.join(Config.APACHE_SITES_ENABLED, conf_file)

    # Path safety check
    if not os.path.abspath(avail_path).startswith(os.path.abspath(Config.APACHE_SITES_AVAILABLE)):
        return False, "Security Error: Path traversal"

    if not os.path.exists(avail_path):
        return False, "Configuration file not found"

    try:
        if enable:
            if not os.path.exists(enabled_path):
                if Config.MODE == 'development' and os.name == 'nt':
                     import shutil
                     shutil.copy(avail_path, enabled_path)
                else:
                    os.symlink(avail_path, enabled_path)
                msg = "enabled"
            else:
                msg = "already enabled"
        else:
            if os.path.exists(enabled_path):
                os.remove(enabled_path)
                msg = "disabled"
            else:
                msg = "already disabled"

        reload_apache()
        return True, f"Domain {msg}"
    except Exception as e:
        return False, str(e)

def delete_domain(domain_name):
    """
    Deletes the configuration file and document root.
    """
    if not is_valid_domain(domain_name):
        return False, "Invalid domain name"

    conf_file = f"{domain_name}.conf"
    avail_path = os.path.join(Config.APACHE_SITES_AVAILABLE, conf_file)
    enabled_path = os.path.join(Config.APACHE_SITES_ENABLED, conf_file)
    doc_root = os.path.join(Config.WEB_ROOT, domain_name)

    # Path safety check
    if not os.path.abspath(doc_root).startswith(os.path.abspath(Config.WEB_ROOT)):
        return False, "Security Error: Path traversal"

    try:
        # Disable first
        if os.path.exists(enabled_path):
            os.remove(enabled_path)

        # Remove config
        if os.path.exists(avail_path):
            os.remove(avail_path)

        # Remove content
        if os.path.exists(doc_root):
            import shutil
            shutil.rmtree(doc_root)

        reload_apache()
        return True, "Domain deleted"
    except Exception as e:
        return False, str(e)

def reload_apache():
    """
    Reloads Apache service.
    """
    try:
        subprocess.run(Config.RELOAD_CMD, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
