

import os
import sys
import getopt
import json
import io

from libe3g.error import *
from libe3g import cryptmanager as cm
from libe3g import cryptmode
from libe3g import log
from libe3g import util



def _init_new_secret_folder(folder_name, usr_pass):
    """ Initialize the on disk structure for a new secret directory with the given name. """

    assert None != folder_name
    assert (isinstance(folder_name, str) or isinstance(folder_name, unicode))

    # example folder_name: "./sf"  shadow >>> "./sf_shadow"

    # if "./sf" is a file - error cant init.
    if os.path.isfile(folder_name):
        raise E3GError("Supplied directory name exists and is a file.")

    shadow_dir = util.get_shadow_name(name=folder_name)

    # if "./sf_shadow" is a file - error cant init.
    if os.path.isfile(shadow_dir):
        raise E3GError("Can't accept the supplied directory name, because its shadow is a file.")

    # if "./sf_shadow" is a non-empty directory - error cant init.
    if os.path.isdir(shadow_dir) and (0 != len(os.listdir(shadow_dir))):
        raise E3GError("Can't accept the supplied directory name, because its shadow is a non-empty folder.")


    # make the secret folder and its shadow.
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    if not os.path.isdir(shadow_dir):
        os.makedirs(shadow_dir)

    # open the .e3g file inside the secret dir for writing.
    dot_e3g_fpath = os.path.join(folder_name, '.e3g')

    dot_e3g = {}
    dot_e3g['salt'] = cm.get_new_random_salt()

    tmp_filenames = os.listdir(folder_name)
    plaintext_filenames = [tmp_fname  for tmp_fname in tmp_filenames if tmp_fname != '.e3g']
    log.vv("file names of files found at src: " + str(plaintext_filenames))


    dot_e3g['src_annon_names'] = [(pfname, cryptmode.get_new_random_filename()) for pfname in plaintext_filenames]
    #log.vvv(dot_e3g['src_annon_names'])


    # now save the .e3g file into './sf' folder
    util.save_dict_as_json_to_pathname(dst_pathname=dot_e3g_fpath, py_dict=dot_e3g)

    # now make shadow files in './sf_shadow' for everything that lives in '.sf_shadow'
    tc = cm.Transcryptor(usr_pass=usr_pass, salt=dot_e3g['salt'])
    tc.encrypt_file(src=dot_e3g_fpath, dst=os.path.join(shadow_dir, '.e3g'))

    for src_name, annon_name in dot_e3g['src_annon_names']:
        src_pathname = os.path.join(folder_name, src_name)
        annon_pathname = os.path.join(shadow_dir, annon_name)
        log.v(src_pathname + ' >>>> ' + annon_pathname)

        tc.encrypt_file(src=src_pathname, dst=annon_pathname)






def _parse_cmdline(arguments):
    """ Given command line arguments to the program are in the arguments list, parse and process them. """

    assert isinstance(arguments, list)
    log.fefr("_parse_cmdline() called with arguments: " + str(arguments))


    # TODO add support 4 these subcommands
    # initsd (init new secret dir)
    # ms (make shadow) (rdycommit) ( no option == everything) (list of files or dirs == just those)
    # us (un-shadow)

    # TODO remove this
    shadow_files = os.listdir('./sf_shadow')
    for shadow_file in shadow_files:
        os.remove(os.path.join('./sf_shadow', shadow_file))
    os.removedirs('./sf_shadow')


    # TODO remove the hard code, ask the user for this.
    usr_pass = 'riscvryzenplz48163264'

    _init_new_secret_folder(folder_name='./sf', usr_pass=usr_pass)
    #_init_new_secret_folder(folder_name='sf', usr_pass=usr_pass)


if "__main__" == __name__:

    _parse_cmdline(sys.argv[1:])
