
import os
import log
import json

def get_shadow_name(name):
    """ Given a directory name or path (like './sf' compute and return the shadow version (like './sf_shadow' """

    log.fefrv("get_shadow_name() called with type(arg), str(arg): " + str(type(name)) + " >>" + str(name) + "<<")

    final_comp = os.path.basename(name)
    dir_comp = os.path.dirname(name)

    # add '.' to the start of final_comp if we wanted to make the shadow a hidden folder.
    #final_comp = '.' + final_comp + '_shadow'
    final_comp = final_comp + '_shadow'

    result = os.path.join(dir_comp, final_comp)

    log.fefrv("get_shadow_name() returning with result: " + str(result))
    return result


def save_dict_as_json_to_pathname(dst_pathname, py_dict):
    """ Given a pathname to a writable file, and a python dict, 
    Serialize the dict as json and save it to the file. """

    log.fefrv('save_dict_as_json_to_pathname() called, args:')
    log.fefrv('dst_pathname: ' + str(dst_pathname) + " py_dict: " + str(py_dict))

    assert isinstance(dst_pathname, str) or isinstance(dst_pathname, unicode)
    assert isinstance(py_dict, dict)

    dot_e3g_fhandle = open(dst_pathname, 'wb')

    json.dump(py_dict, dot_e3g_fhandle, ensure_ascii=False, indent=4, sort_keys=True)

    # alternative using dumps method.
    # dot_e3g_serialized = json.dumps(py_dict, ensure_ascii=False, indent=4, sort_keys=True)
    # log.vvv('dumping serialized dict to file: ' + str(dst_pathname))
    # log.vvv(dot_e3g_serialized)
    #dot_e3g_fhandle.write( dot_e3g_serialized )

    dot_e3g_fhandle.flush()
    dot_e3g_fhandle.close()

    log.fefrv('save_dict_as_json_to_pathname() returning')

if '__main__' == __name__:

    get_shadow_name('./sf')