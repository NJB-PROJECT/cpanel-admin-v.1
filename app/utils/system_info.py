import psutil
import platform
import datetime

def get_system_stats():
    """
    Returns a dictionary containing CPU, Memory, Disk, and System info.
    """

    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)

    # Memory
    mem = psutil.virtual_memory()
    mem_total_gb = round(mem.total / (1024**3), 2)
    mem_used_gb = round(mem.used / (1024**3), 2)
    mem_percent = mem.percent

    # Disk
    disk = psutil.disk_usage('/')
    disk_total_gb = round(disk.total / (1024**3), 2)
    disk_used_gb = round(disk.used / (1024**3), 2)
    disk_percent = disk.percent

    # System Info
    uname = platform.uname()
    os_info = f"{uname.system} {uname.release}"
    node_name = uname.node
    uptime_seconds = int(datetime.datetime.now().timestamp() - psutil.boot_time())
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))

    return {
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count
        },
        'memory': {
            'total': mem_total_gb,
            'used': mem_used_gb,
            'percent': mem_percent
        },
        'disk': {
            'total': disk_total_gb,
            'used': disk_used_gb,
            'percent': disk_percent
        },
        'system': {
            'os': os_info,
            'hostname': node_name,
            'uptime': uptime_str
        }
    }
