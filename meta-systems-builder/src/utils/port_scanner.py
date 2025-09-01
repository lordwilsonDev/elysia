import socket
from typing import Optional

def find_free_port(start_port: int = 8000, end_port: int = 8999) -> Optional[int]:
    """Find a free port in the specified range"""
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    return None

def check_port_availability(port: int) -> bool:
    """Check if a specific port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except OSError:
            return False
