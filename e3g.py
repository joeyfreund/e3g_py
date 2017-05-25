#! /usr/bin/env python


import os
import sys
import argparse

from libe3g.error import *
from libe3g import cryptmanager as cm
from libe3g import cryptmode
from libe3g import log
from libe3g import util



def _init_new_secret_folder222(folder_name, usr_pass):
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

    # .e3g_public file resides in './sf' and also in './sf_shadow' in plain text. public items go in it. (i.e kdf salt)
    dot_e3g_public = {}
    dot_e3g_public['salt'] = cm.get_new_random_salt()

    # now that we have the salt and the user pass make a transcryptor obj that can encrypt and decrypt things.
    tc = cm.Transcryptor(usr_pass=usr_pass, salt=dot_e3g_public['salt'])

    secret_folder_current_files = os.listdir(folder_name)

    plaintext_filenames = []
    for sf_filename in secret_folder_current_files:
        if ('.e3g_public' != sf_filename) and ('.e3g_protected' != sf_filename):
            plaintext_filenames.append(sf_filename)
        else:
            log.vv("found e3g file: " + sf_filename)


    log.vv("file names of files found at src(excluding .e3g files): " + str(plaintext_filenames))

    # now we have files whose name is in plaintext_filenames list + the two .e3g files.

    # .dot_e3g_protected file resides in './sf' and has its cipher text version in './sf_shadow'
    dot_e3g_protected = {}
    filename_mappings = [(pfname, cryptmode.get_new_random_filename()) for pfname in plaintext_filenames]
    dot_e3g_protected['filename_mappings'] = filename_mappings
    #log.vvv(dot_e3g['filename_mappings'])


    # now save the .e3g_public file into both './sf' and './sf_shadow' folder
    util.save_dict_as_json_to_pathname(dst_pathname=os.path.join(folder_name, '.e3g_public'), py_dict=dot_e3g_public)
    util.save_dict_as_json_to_pathname(dst_pathname=os.path.join(shadow_dir, '.e3g_public'), py_dict=dot_e3g_public)

    # now save the .e3g_protected file into './sf' and its ciphertext version into './sf_shadow' folder
    util.save_dict_as_json_to_pathname(dst_pathname=os.path.join(folder_name, '.e3g_protected'), py_dict=dot_e3g_protected)
    tc.encrypt_file(src=os.path.join(folder_name, '.e3g_protected'), dst=os.path.join(shadow_dir, '.e3g_protected'))

    # now make shadow files in './sf_shadow' for everything that lives in '.sf'
    for src_name, annon_name in dot_e3g_protected['filename_mappings']:
        src_pathname = os.path.join(folder_name, src_name)
        annon_pathname = os.path.join(shadow_dir, annon_name)
        log.v(src_pathname + ' >>>> ' + annon_pathname)

        tc.encrypt_file(src=src_pathname, dst=annon_pathname)



def _process_rdycommit_subcommand(dest):
    """ Process the rdycommit subcommand. May block and ask user some questions. """

    log.fefr("_process_rdycommit_subcommand() called with dest: " + str(dest))

    pass



def _process_init_subcommand(dest):
    """ Process the init subcommand. May block and ask user some questions. 
    dest is the name of the new secret folder to be inited. 
    
    """

    log.fefr("_process_init_subcommand() called with dest: " + str(dest))

    sf_name = dest
    log.v("destination folder is: " + str(sf_name))

    if None == sf_name:
        print "Error: No destination name supplied. Plz supply a name for your encrypted secret folder."
        sys.exit(2)


    assert (isinstance(sf_name, str) or isinstance(sf_name, unicode))

    # example sf_name: "./sf"  shadow >>> "./sf_shadow"

    # if "./sf" is a file - error cant init.
    if os.path.isfile(sf_name):
        print "Error: Supplied name exists and is a file."
        sys.exit(2)

    shadow_dir = util.get_shadow_name(name=sf_name)

    # if "./sf_shadow" is a file - error cant init.
    if os.path.isfile(shadow_dir):
        print "Error: Can't accept the supplied name, because its shadow is a file."
        sys.exit(2)

    # if "./sf_shadow" is a non-empty directory - error cant init.
    if os.path.isdir(shadow_dir) and (0 != len(os.listdir(shadow_dir))):
        print "Error: Can't accept the supplied name, because its shadow is a non-empty folder."
        sys.exit(2)

    # make the secret folder and its shadow.
    if not os.path.isdir(sf_name):
        os.makedirs(sf_name)

    if not os.path.isdir(shadow_dir):
        os.makedirs(shadow_dir)


    # .e3g_public file resides in './sf' and also in './sf_shadow' in plain text. public items go in it. (i.e kdf salt)
    dot_e3g_public = {}
    dot_e3g_public['salt'] = cm.get_new_random_salt()


    # now save the .e3g_public file into both './sf' and './sf_shadow' folder
    util.save_dict_as_json_to_pathname(dst_pathname=os.path.join(sf_name, '.e3g_public'), py_dict=dot_e3g_public)

    # now make a gitignore for './sf' to make sure git does not track the plaintext files.
    sf_gitignore_fh = open(os.path.join(sf_name, '.gitignore'), 'wb')
    sf_gitignore_fh.write('## Git should not track the content of your secret directory. Only its shadow version. \n')
    sf_gitignore_fh.write('*\n\n')
    sf_gitignore_fh.flush()
    sf_gitignore_fh.close()







def _process_checkout_subcommand(dest):
    """ Process the checkout subcommand. May block and ask user some questions. """

    log.fefr("_process_checkout_subcommand() called with dest: " + str(dest))

    pass


def _parse_cmdline(arguments):
    """ Given command line arguments to the program are in the arguments list, parse and process them. """

    parser = argparse.ArgumentParser(description='E3G - End to End Encrypted Git')
    parser.add_argument("subcmd1", help="what should e3g do", choices=['init', 'rdycommit', 'checkout'])
    parser.add_argument("destination", help="which folder to init, or rdy 4 commit, or checkout", nargs='?')
    args = parser.parse_args()

    # print type(args) returns  <class 'argparse.Namespace'>
    if 'init' == args.subcmd1:
        log.vvv(">>>> init sub command called.")
        _process_init_subcommand(dest=args.destination)

    elif 'rdycommit' == args.subcmd1:
        log.vvv(">>>> rdycommit sub command called.")

    elif 'checkout' == args.subcmd1:
        log.vvv(">>>> checkout sub command called.")

    #log.vvv("argparse args: " + str(args))



def debug_run_1(arguments):
    """ Given command line arguments to the program are in the arguments list, parse and process them. """

    assert isinstance(arguments, list)
    log.fefr("_parse_cmdline() called with arguments: " + str(arguments))


    # TODO add support 4 these subcommands
    # initsd (init new secret dir)
    # ms (make shadow) (rdycommit) ( no option == everything) (list of files or dirs == just those)
    # us (un-shadow)

    # TODO remove this, this is just for debug.
    try:
        shadow_files = os.listdir('./sf_shadow')
        for shadow_file in shadow_files:
            os.remove(os.path.join('./sf_shadow', shadow_file))
        #os.removedirs('./sf_shadow')
    except:
        log.vv("Error occurred in trying to clear the shadow folder.")
        pass

    # TODO remove the hard code, ask the user for this.
    usr_pass = 'riscvryzenplz48163264'

    #_init_new_secret_folder(folder_name='./sf', usr_pass=usr_pass)
    #_init_new_secret_folder(folder_name='sf', usr_pass=usr_pass)




if "__main__" == __name__:

    #_parse_cmdline(sys.argv[1:])

    _parse_cmdline(sys.argv[1:])


