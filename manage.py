'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
import logging
import os
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("manage.py")
global app

def showUsage():
    print("""Usage:
    python manage.py <Option>
    python manage.py syncdb    # Create DB
    python manage.py init      # Init Demo datas
    python manage.py clean     # Clean virtenv
    python manage.py prepare   # Prepare virtenv
    """)
    sys.exit()

def opt_syncdb():
#     src = os.path.join(BASE_DIR, 'mysite', 'demo.sqlite3')
#     dst = os.path.join(BASE_DIR, 'mysite', 'db.sqlite3')
#     shutil.rmtree(dst, ignore_errors=True)
#     shutil.copy(src, dst)
    pass

def opt_init():
    pass

def opt_clean():
    ENV_DIR = "env"
    if os.path.isdir(ENV_DIR):
        shutil.rmtree(ENV_DIR)

def opt_test():
    pass

def opt_prepare():
    _assert_cmd_exist("pip")
    os.system("pip install virtualenv")
    
    opt_syncdb()
    opt_init()
    
    opt_prepare_theme()

def opt_prepare_theme():
    pass

def _assert_cmd_exist(cmd):
    try:
        subprocess.call(cmd)
    except Exception as e:
        log.warning("{}->{}".format(type(e), e.message))
        log.error("Command '{}' not exist!".format(cmd))
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        showUsage()

    selfModule = __import__(__name__)
    optFunName = "opt_" + sys.argv[1].strip()
    if optFunName not in selfModule.__dict__:
        showUsage()

    if BASE_DIR.strip():
        os.chdir(BASE_DIR)
    selfModule.__dict__[optFunName](*sys.argv[2:])
