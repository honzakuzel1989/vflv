"""
Verificators
"""

import re

def verify_password(password):
    # delka alespon 4
    # alespon jedno cislo
    # alespon jedno pismeno
    if len(password) < 4:
        return (False, 'Invalid len of new password (min=4)')
    if not re.search('[a-zA-Z]', password):
        return (False, 'Invalid new password (must contain a letter [a-zA-Z])')
    if not re.search('[0-9]', password):
        return (False, 'Invalid new password (must contain a number [0-9])')
    return (True, None)

def verify_voting_values(form_voting_items):
    # max 3 hlasovani
    # min hodnota 1
    # max hodnota 3
    # zadne stejne hodnoty
    cnt = 0
    ivals = []
    for val in form_voting_items:
        if val:
            cnt += 1
            ival = 0
            
            try:
                ival = int(val)
            except ValueError:
                return (False, 'Invalid input of voting (values=1,2,3,4)')
            if not 0 < ival < 4:
                return (False, 'Invalid value of voting (min=1, max=3)')
            if ival in ivals:
                return (False, 'Invalid value of voting (values must be unique)')
            ivals.append(ival)
    retval = 0 < cnt < 4
    return (True, None) if 0 < cnt < 4 else (False, 'Invalid number of votings (min=1, max=3)')
