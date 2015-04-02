"""
Helpers
"""

from datetime import datetime
from hashlib import sha256 as sha

def compute_hash_in_hex(password):
    hash_object = sha(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def get_time_in_s():
    dt_trunc = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_in_s = int((dt_trunc - datetime(1970,1,1)).total_seconds())
    return dt_in_s

def get_current_time_in_s():
    dt_now_in_s = get_time_in_s(datetime.now())
    return dt_now_in_s

def get_current_year():
    return datetime.now().year
