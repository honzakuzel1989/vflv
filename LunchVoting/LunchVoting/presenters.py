"""
Presenters
"""

import dal
import helpers as h
import verificators as v

def check_auth(username, password):
    """Check authorization"""
    entries = dal.get_user_by_username(username)

    if len(entries) != 1:
        return (False, 'Invalid username')

    pass_h = entries[0]['pass']
    verif = pass_h == h.compute_hash_in_hex(password)

    return (True, None) if verif else (False, 'Invalid password')
    
def get_pubs_items(pubs, day_votings, day_sums):
    pubs_items = []
    for p in pubs:
        has_voting = False
        for dv in day_votings:
            if p['title'] == dv['pub']:
                pubs_items.append((p, dv, day_sums[p['id']]))
                has_voting = True
                break
        if not has_voting:
            pubs_items.append((p, None, day_sums[p['id']]))
    return pubs_items

def vote(user, day_voting, form_voting_items):
    retval, error = v.verify_voting_values(form_voting_items)
    if not retval:
        return (False, error)

    if day_voting:
        dal.delete_actual_voting(user)
        
    for (pub_id, rating) in form_voting_items:
        if rating:
            dal.insert_voting(user, pub_id, int(rating))

    return (True, None)
