
import database as d

def get_user_by_username(username):
    db = d.get_db()
    cur = db.execute('select pass from users where name=?', [username])
    entries = cur.fetchall()
    return entries
   
def get_pubs():
    db = d.get_db()
    cur = db.execute('select * from pubs')
    entries = cur.fetchall()
    return entries
