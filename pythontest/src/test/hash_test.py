#-*- coding: UTF-8 -*-
'''
Created on 2015.7.17

@author: gong_shengmin
'''
import hashlib

def calc_md5(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()



#print calc_md5(str(112345))


db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}

def login(user, password):
    md5 = hashlib.md5()
    md5.update(password)
    if user in db.keys():
        if db[user] == md5.hexdigest():                
            return True
        else:
            return  False
    print "no this user"
    return False 

#print login('michael','123456')


dbsafe = {}
def loginsafe(user, password):
    md5 = hashlib.md5()
    md5.update(password + user + 'the-Salt')    
    if user in dbsafe.keys():
        if dbsafe[user] == md5.hexdigest():                
            return True
        else:
            return  False
    print "no this user"
    return False 

def register(username,password):
    if username in dbsafe.keys():
        print "the user exist!"
    else:
        dbsafe[username] = calc_md5(password + username + 'the-Salt')
register('snail','135764')
register('sudo','19891228')
print dbsafe
print  loginsafe('snail','135764')  
print  loginsafe('sudo','19891228')  
