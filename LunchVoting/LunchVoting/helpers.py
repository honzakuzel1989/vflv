"""
Helpers
"""

from datetime import datetime
from hashlib import sha256 as sha

def compute_hash_in_hex(password):
    hash_object = sha(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig
    
def get_current_time_in_s():
    dt_now = datetime.now()
    dt_now_trunc = dt_now.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_now_in_s = int((dt_now_trunc - datetime(1970,1,1)).total_seconds())
    return dt_now_in_s
