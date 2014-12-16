import pickle
import hashlib, uuid
import os
import logging

log = logging.getLogger('rhizi')

def add_user_login(config, u, p):
    htpasswd_path = config.htpasswd_path

    if False == os.path.exists(htpasswd_path):
        with open(htpasswd_path, 'wb') as f:
            pickle.dump({}, f)

    with open(htpasswd_path, 'rb') as f:
        data = f.read()
        pw_db = pickle.loads(data)

    with open(htpasswd_path, 'wb') as f:
        salt = config.secret_key
        pw_db[u] = hash_pw(str(p), salt)
        pickle.dump(pw_db, f)

    log.info('htpasswd db: added entry: user: %s, pw: %s...' % (u, pw_db[u][:5]))

def hash_pw(pw_str, salt_str):
    salt = hashlib.sha512(salt_str).hexdigest()
    ret = hashlib.sha512(pw_str + salt).hexdigest()
    return ret

def validate_login(config, u, p):
    htpasswd_path = config.htpasswd_path

    salt = config.secret_key

    with open(htpasswd_path) as f:
        pw_db = pickle.load(f)

        existing_pw_hash = pw_db.get(u)
        if None == existing_pw_hash:
            raise Exception('Not autorhized')

        if hash_pw(p, salt) != existing_pw_hash:
            raise Exception('Not autorhized')

