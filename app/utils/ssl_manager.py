import subprocess
import shlex
from app.config import Config

def install_ssl(domain_name, email):
    """
    Runs Certbot to obtain an SSL certificate.
    """
    # Security: Ensure inputs are simple strings to prevent injection
    # Although subprocess.run with list args handles most, we should strictly validate format beforehand.
    # The caller (main.py) should have validated domain syntax.

    # Construct command as a list of arguments (safer than shell=True)
    # We need to split the base command (Config.CERTBOT_CMD) which might be "sudo certbot --apache"
    base_cmd = shlex.split(Config.CERTBOT_CMD)

    cmd_args = base_cmd + [
        '-d', domain_name,
        '--non-interactive',
        '--agree-tos',
        '-m', email,
        '--redirect'
    ]

    try:
        # shell=False is the default, which prevents shell injection
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        if result.returncode == 0:
            return True, "SSL Installed successfully!\n" + result.stdout
        else:
            return False, "SSL Installation Failed:\n" + result.stderr
    except Exception as e:
        return False, f"System Error: {str(e)}"
