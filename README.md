# Jarvis Clouding Control Panel

A simple, lightweight control panel for managing Apache Virtual Hosts, monitoring system stats, and handling SSL on a Kali Linux server.

## Features
*   **Dashboard**: Monitor CPU, RAM, and Disk usage in real-time.
*   **Domain Manager**: Create, Enable, Disable, and Delete websites (Apache Virtual Hosts).
*   **Logs**: View Apache Access and Error logs.
*   **SSL Manager**: One-click Let's Encrypt SSL installation via Certbot.

## Prerequisites (On Kali Linux)

Before running the panel, ensure you have the necessary system packages installed:

```bash
sudo apt update
sudo apt install apache2 certbot python3-certbot-apache python3-pip python3-venv -y
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd jarvis-panel
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application automatically detects if it's running in production or development mode.

*   **Production**: If running on the server, it targets `/etc/apache2` and executes real system commands.
*   **Development**: If the environment variable `APP_MODE` is not set or set to `development`, it uses a local `mock_fs` folder to simulate file operations.

To run in **Production Mode** (REQUIRED for actual server management):

```bash
export APP_MODE=production
```

## Running the Panel

Since the panel needs to modify system files (Apache configs) and restart services, it must be run with **root privileges** (sudo).

1.  **Activate venv (if not already):**
    ```bash
    source venv/bin/activate
    ```

2.  **Run with sudo (preserving environment variables):**
    ```bash
    sudo APP_MODE=production ./venv/bin/python app/main.py
    ```
    *Note: Pointing directly to the python executable inside the venv ensures dependencies are found even under sudo.*

3.  **Access the Panel:**
    Open your browser and navigate to `http://<YOUR-SERVER-IP>:5000`

## Security Note

This panel allows system-level changes.
*   Ensure the port 5000 is firewalled if not needed externally, or use SSH tunneling.
*   **Version 1.0 does not have authentication.** Do not expose this to the public internet without adding a login mechanism or restricting access via IP.

## Troubleshooting

*   **Apache not reloading?** Check `sudo systemctl status apache2`.
*   **SSL Fails?** Ensure port 80 is open and your domain DNS points to this server.
