

import os
import sys
import getopt


from libe3g import cryptmanager as cm
from libe3g import log







def _parse_cmdline(arguments):
    """ Given command line arguments to the program are in the arguments list, parse and process them. """

    assert isinstance(arguments, list)
    log.fefr("_parse_cmdline() called with arguments: " + str(arguments))


    # TODO add support 4 these subcommands
    # initsd (init new secret dir)
    # ms (make shadow) (rdycommit) ( no option == everything) (list of files or dirs == just those)
    # us (un-shadow)


    #tc = cm.Transcryptor(usr_pass='riscvryzenplz481632', salt=)




if "__main__" == __name__:

    _parse_cmdline(sys.argv[1:])
