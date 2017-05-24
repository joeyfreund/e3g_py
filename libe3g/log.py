

from cryptmode import should_print_insecure_log_msgs


#-----------------------------------------------------------------------------------------------------------------------
def fefrv(msg, label=True):
    """ Print log msgs for "function entry, function return verified" category. """

    if True:
        return

    final_msg = None

    if label:
        final_msg = 'fefrv: ' + str(msg)
    else:
        final_msg =  str(msg)

    print final_msg


#-----------------------------------------------------------------------------------------------------------------------
def fefr(msg, label=True):
    """ Print log msgs for "function entry, function return" category. """

    final_msg = None

    if label:
        final_msg = 'fefr: ' + str(msg)
    else:
        final_msg =  str(msg)

    print final_msg


#-----------------------------------------------------------------------------------------------------------------------
def vvv(msg, label=True):
    """ print log msgs that are in "triple verbose" category. """

    final_msg = None

    if label:
        final_msg = 'vvv: ' + str(msg)
    else:
        final_msg = str(msg)

    print final_msg


#-----------------------------------------------------------------------------------------------------------------------
def vv(msg, label=True):
    """ print log msgs that are in "double verbose" category. """

    final_msg = None

    if label:
        final_msg = 'vv: ' + str(msg)
    else:
        final_msg = str(msg)

    print final_msg


#-----------------------------------------------------------------------------------------------------------------------
def v(msg, label=True):
    """ print log msgs that are in "single verbose" category. """

    final_msg = None

    if label:
        final_msg = 'v: ' + str(msg)
    else:
        final_msg = str(msg)

    print final_msg


#-----------------------------------------------------------------------------------------------------------------------
def hazard(msg, label=True):
    """ print log msgs that are in "hazardous" category. These msgs should not be printed in a production build. """

    if not should_print_insecure_log_msgs:
        return

    final_msg = None

    if label:
        final_msg = '***** hazardous msg: ' + str(msg)
    else:
        final_msg = str(msg)

    print final_msg



