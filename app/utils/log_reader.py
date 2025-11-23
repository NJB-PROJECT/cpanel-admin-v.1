import os
from app.config import Config

def get_log_content(log_type='access', lines=50):
    """
    Reads the last N lines of the specified log file.
    log_type: 'access' or 'error'
    """
    log_file = "access.log" if log_type == 'access' else "error.log"
    path = os.path.join(Config.APACHE_LOG_DIR, log_file)

    if not os.path.exists(path):
        # Create dummy log if not exists (for dev mode)
        if Config.MODE != 'production':
            with open(path, 'w') as f:
                f.write(f"[Info] This is a mock {log_type} log.\n")
        else:
            return [f"Log file not found: {path}"]

    try:
        # Simple implementation to read last N lines
        # efficient enough for small N
        with open(path, 'r', errors='ignore') as f:
            content = f.readlines()
            return content[-lines:]
    except Exception as e:
        return [f"Error reading log: {str(e)}"]
