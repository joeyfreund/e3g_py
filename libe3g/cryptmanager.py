
# TODO
# NOTE
## ATTENTION: if _DBG_MODE is true, the system is not secure.
_DBG_MODE = False


import os
import log

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat import backends

backend = backends.default_backend()





def _get_random_bytes(size):
    """ Return size many bytes. This is from a seeded sequence In debug mode. and from the OS random source otherwise.
     ATTENTION: in debug mode the system is not secure. 
     """

    if _DBG_MODE:
        temp = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        factor = (size // len(temp)) + 1
        temp2 = temp * factor
        return temp2[:size]

    return os.urandom(size)

def get_new_random_salt():
    """ Find a suitable random bit pattern to be used as salt for key derivation, and return it.
     
     Result is hex encoded for easy transport, viewing. It should be hex decoded back down to bytes before getting
     passed to the cryptography library functions. This module takes care of that. Functions of this module 
     return hex encoded values, and hex decode their argument values whenever suitable.
     
     
     Note the salt need not be secret, and need not be that random. just something to be passed to kdf along with 
     user password, to make the encryption keys coming out of kdf, not pre-computable 
     (i.e. an attack against a 2nd repo should start from scratch and not benefit from another attack against 
     a different repo from a different time. 
     """

    result = _get_random_bytes(size=32).encode('hex')

    log.fefr("get_new_random_salt() returning. result (as hex encoded): " + str(result))
    return result

class Transcryptor(object):
    """ Helper class for encrypting and decrypting files safely with a symmetric cipher and  user provided  
    password (user pass, is the pass b4 kdf applied). 
    """

    def __init__(self, usr_pass, salt, progress_callback=None):
        """ Init a new Transcryptor object. Applies the key derivation function to user password, and 
        saves it this object for future encrypt, decrypt operations. 
        
        To lose the key simply destroy this object from memory. 
        
        Since the key derivation function is intentionally compute-intensive this init call might take 
        a while to return. 
        
        """
        super(Transcryptor, self).__init__()





    def encrypt_file(self, src, dst):
        """ Given the pathname to a source file, encrypt it and save it into another file whose pathname is dst.  """


        pass

    def decrypt_file(self, src, dst):
        """ Given the pathname to a source file, decrypt it and save it into another file whose pathname is dst.  """


        pass

