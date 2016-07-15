"""
DAL
"""

import database as d
import helpers as h

def get_user_by_username(username):
    db = d.get_db()
    cur = db.execute('select pass from users where name=?', [username])
    entries = cur.fetchall()
    return entries
   
def get_pubs():
    db = d.get_db()
    cur = db.execute('select * from pubs where visible!=?', [0])
    entries = cur.fetchall()
    return entries
    
def get_actual_voting_for_all_user():
    db = d.get_db()
    cur = db.execute('select votings.*, users.nickname from votings, users where date=? and user=name', 
        [h.get_current_time_in_s()])
    entries = cur.fetchall()
    return entries
    
def get_actual_voting_for_user(user):
    db = d.get_db()
    cur = db.execute('select * from votings where date=? and user=?', 
        [h.get_current_time_in_s(), user])
    entries = cur.fetchall()
    return entries
    
def get_actual_sum(pub_id):
    db = d.get_db()
    cur = db.execute('select sum(rating) as psum from votings where date=? and pub=?', 
        [h.get_current_time_in_s(), pub_id])
    psum = cur.fetchall()[0]['psum']
    return psum if psum else 0
    
def update_password(user, new_pass):
    db = d.get_db()
    cur = db.execute('update users set pass=? where name=?', 
        [h.compute_hash_in_hex(new_pass), user])
    db.commit()
    
def delete_actual_voting(user):
    db = d.get_db()
    db.execute('delete from votings where date=? and user=?', 
        [h.get_current_time_in_s(), user])
    db.commit()

def insert_voting(user, pub_id, rating):
    db = d.get_db()
    cur = db.execute('select * from pubs where id = ?', [pub_id])
    pubs = cur.fetchall()

    db.execute('insert into votings (date, user, pub, rating) values (?, ?, ?, ?)', 
        [h.get_current_time_in_s(), user, pubs[0]['title'], rating])
    db.commit()
