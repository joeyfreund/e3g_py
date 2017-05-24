


import os
import log
import cryptmode







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

    result = cryptmode.get_new_random_salt_for_current_mode().encode('hex')

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

        kdf = cryptmode.make_kdf_for_current_mode(salt=salt.decode('hex'))

        self.encryption_key = kdf.derive(key_material=usr_pass)

        log.v('encryption key hex encoded: ' + self.encryption_key.encode('hex'))


        # this returns None if ok, else raises InvalidKey error, also u need a new kdf object,
        # they destroy themselves after one use.
        # kdf = cryptmode.make_kdf_for_current_mode(salt=salt.decode('hex'))
        # kdf.verify(key_material=usr_pass, expected_key=self.encryption_key)


    def encrypt_file(self, src, dst):
        """ Given the pathname to a source file, encrypt it and save it into another file whose pathname is dst.  """

        log.fefr('encrypt_file() called, with src: >>{}<< dst: >>{}<<'.format(src, dst) )




    def decrypt_file(self, src, dst):
        """ Given the pathname to a source file, decrypt it and save it into another file whose pathname is dst.  """


        pass

