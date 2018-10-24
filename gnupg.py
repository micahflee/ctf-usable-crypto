import os
from subprocess import Popen, PIPE

class GnuPG(object):
    def __init__(self):
        self.gpg_path = '/usr/bin/gpg'

        # Create a homedir to work in
        self.homedir = 'homedir'
        if not os.path.exists(self.homedir):
            os.makedirs(self.homedir, 0700)

    def _gpg(self, args, input=None):
        p = Popen([self.gpg_path, '--batch', '--no-tty', '--homedir', self.homedir] + args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        if input:
            (out, err) = p.communicate(input)
        else:
            p.wait()
            out = p.stdout.read()
            err = p.stderr.read()

        return out, err

    def import_key(self, pubkey):
        self._gpg(['--import'], pubkey)

    def get_fingerprint(self, pubkey):
        out, err = self._gpg(['--with-colons', '--with-fingerprint'], pubkey)

        for line in out.split('\n'):
            if line.startswith('fpr:'):
                fp = line.split(':')[9]
                return fp

        return False
    
    def get_uid(self, pubkey):
        out, err = self._gpg(['--with-colons', '--with-fingerprint'], pubkey)
        
        for line in out.split('\n'):
            if line.startswith('pub:'):
                fp = line.split(':')[9]
                return fp

        return False

    def encrypt(self, message, fingerprint):
        out, err = self._gpg(['--armor', '--no-emit-version', '--no-comments', '--trust-model', 'always', '--encrypt', '--recipient', fingerprint], message)
        return out

