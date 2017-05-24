
# This module is where all the cryptographic defaults live.
# changing a hashing algorithm from sha256 to sha512 should require changes to this file only.
# the entire rest of the system should not assume anything about choice of cipher, hash, length of something .....
# all of these defaults should be set/changed in this module only.


# TODO
# NOTE
## ATTENTION: if any of these insecure modes are enabled, the system is not secure.

_INSECURE_RAND_SRC = False

_INSECURE_LOG_MSGS = True
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
import os
import log

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat import backends





def should_print_insecure_log_msgs():
    """ Return true when insecure log msgs are desired (during development) returns false in production """

    return _INSECURE_LOG_MSGS



def is_in_insecure_rand_mode():
    """ Return true when the system is running in the insecure random source. False otherwise. 
     Also prints warning to console every time mode is queried.
     
     This method should return False in a production environment.
     """

    if _INSECURE_RAND_SRC:
        print "*******  Warning: system is in INSECURE RAND SRC MODE. (use this only in development). "

        return True

    return False


def make_kdf_for_current_mode(salt):
    """ Make and return kdf object, that can be used to derive encryption keys from a user pass and a salt. 
    Depending on which mode and cryptography defaults the system is running in this will return a suitable kdf.
    """

    assert None != salt

    return _make_kdf_1(salt=salt)


def _make_kdf_1(salt):
    """ Make and return kdf object, using the 1st set of defaults. .
    """

    assert None != salt

    backend = backends.default_backend()
    algorithm = hashes.SHA256()
    length = 32
    iterations = 1000 * 1000   # 1 million rounds of sha256

    kdf = PBKDF2HMAC(algorithm=algorithm, length=length, salt=salt, iterations=iterations, backend=backend)
    return kdf

def _make_kdf_2(salt):
    """ Make and return kdf object, using the 2nd set of defaults. .
    """

    assert None != salt

    backend = backends.default_backend()
    algorithm = hashes.SHA512()
    length = 32
    iterations = 2000 * 1000 # 2 million rounds of sha512

    kdf = PBKDF2HMAC(algorithm=algorithm, length=length, salt=salt, iterations=iterations, backend=backend)
    return kdf



def get_new_random_salt_for_current_mode():
    """ Return a new salt for key derivation. Based on the defaults of the current crypt mode.
     """
    log.fefrv("get_new_random_salt_for_current_mode() called")

    size = 32

    if is_in_insecure_rand_mode():
        temp = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        factor = (size // len(temp)) + 1
        temp2 = temp * factor
        return temp2[:size]

    return os.urandom(size)



def get_new_random_filename():
    """ Return a new random filename. This from os urandom in production mode and predictable sequence otherwise. """

    size = 48

    result = os.urandom(size).encode('hex')

    log.fefrv("get_new_random_filename() returning. new file name is: \n " + result)

    return result
