FLAG = '{FLAG_tinykeyspaceisbadforbusiness12345}'

from flask import Flask, render_template, request
from gnupg import GnuPG

app = Flask(__name__)
gpg = GnuPG()

def fingerprint_to_color(fp):
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    max_num = int('ffffffffffffffffffffffffffffffffffffffff', 16)
    blocksize = max_num / len(colors)

    fp_num = int(fp, 16)
    index = fp_num / blocksize
    if index == len(colors):
        index -= 1
    return colors[index]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    msg = request.form['msg'].strip()
    if msg.startswith('-----BEGIN PGP PUBLIC KEY BLOCK-----'):
        pubkey = msg
        gpg.import_key(pubkey)
        fp = gpg.get_fingerprint(pubkey)
        uid = gpg.get_uid(pubkey)

        if not fp:
            return "Weird that public key isn't working for me. Ugh PGP is hard. Can you try again?"
        try:
            color = fingerprint_to_color(fp)
        except:
            return "Weird that public key isn't working for me. Ugh PGP is hard. Can you try again?"

        if uid != "Dept of National Security Agent <agent@dns.spy>":
            return "What are you trying to pull? The name on this key isn't even \"Dept of National Security Agent <agent@dns.spy>\". It's \"{}\".".format(uid)
        if color != 'blue':
            return "What are you trying to pull? This key is {}, not blue.".format(color)

        # success
        plaintext = 'Great, we have a secure channel. Here is the thing I wanted to tell you so badly.\n\n{}\n'.format(FLAG)
        ciphertext = gpg.encrypt(plaintext, fp)
        return 'Ok great, it worked this time! Here is your message.\n\n{0}'.format(ciphertext)

    elif msg.startswith('-----BEGIN PGP PRIVATE KEY BLOCK-----'):
        pubkey = msg
        gpg.import_key(pubkey)
        return "I'm a PGP noob but even I realize that you sent me your secret key. I'll just log this for later. Can you please send me the right public key though?"

    return "Sorry, no time to chat. I just need you to send me the right PGP public key."


@app.route('/easyverify', methods=['GET', 'POST'])
def easyverify():
    if request.method == 'POST':
        pubkey = request.form['pubkey'].strip()
        if pubkey.startswith('-----BEGIN PGP PUBLIC KEY BLOCK-----'):
            gpg.import_key(pubkey)
            fp = gpg.get_fingerprint(pubkey)
            if not fp:
                return render_template('easyverify.html', error='Invalid public key.')

            # now we have a fingerprint, convert it to a color
            try:
                color = fingerprint_to_color(fp)
                return render_template('easyverify.html', color=color, fp=fp)

            except:
                return render_template('easyverify.html', error='Something went wrong.')

        elif pubkey.startswith('-----BEGIN PGP PRIVATE KEY BLOCK-----'):
            gpg.import_key(pubkey)
            return render_template('easyverify.html', error='Looks like you submitted a secret key instead of a public key. Oops. You might want to revoke that key now...')

        else:
            return render_template('easyverify.html', error='Invalid public key.')
    else:
        return render_template('easyverify.html')

if __name__ == '__main__':
    app.run(debug=False)
