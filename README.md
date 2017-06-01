# e3g_py

## version 0.1 alpha
concept showcase for using end to end encryption with a distributed version control system.

## to create a new 'secret folder' (named sf for example) within a git repo run

```sh
$ e3g.py init sf
```

this will create two directories: `./sf/` and `./sf_shadow/`

it will also put a `.gitignore` file in `./sf/` telling git to ignore everything there. 

now proceed to put your private files in `./sf/` directory. you can work with these the usual way, just make sure to run the `rdy` command before commiting things into git, like this:

```sh
$ e3g.py rdy sf
```

This will ask for your password and create ciphertext version of your files and put them into the `./sf_shadow/` directory.
now you can commit and push to github. 

when cloning/pulling the shadow directory will receive the updated ciphertext versions of the files. Now run the checkout command to extract the plaintext, like this:

```sh
$ e3g.py checkout sf
```

This will also ask for password. if the password is wrong or the ciphertext files have been tampered with an error will be raised. 

## trouble shooting errors, dependencies 
make sure `python2` is installed on the system and `e3g.py` file is executable. (alternatively run `$ python e3g.py` ....)

the python cryptography library is also needed. 

```sh
$ pip install cryptography
```







