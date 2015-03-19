
from hashlib import sha256 as sha

def compute_hash_in_hex(password):
    hash_object = sha(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig
