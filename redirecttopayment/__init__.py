from otree.api import *

from Crypto.Cipher import AES
from Crypto import Random
import base64
import binascii
import json



class Constants(BaseConstants):
    name_in_url = 'redirect_pay'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

# FUNCTIONS

def cryptodome_encrypt(data, passphrase):
    """
        # https://gist.github.com/eoli3n/d6d862feb71102588867516f3b34fef1
         Encrypt using AES-256-CBC with random/shared iv
        'passphrase' must be in hex, generate with 'openssl rand -hex 32'
         Encrypt using AES-128-CBC with random/shared iv
        'passphrase' must be in hex, generate with 'openssl rand -hex 16'
    """
    
    try:
        key = binascii.unhexlify(passphrase)
        pad = lambda s : s+chr(16-len(s)%16)*(16-len(s)%16)
        iv = Random.get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_64 = base64.b64encode(cipher.encrypt(pad(data).encode())).decode('ascii')
        iv_64 = base64.b64encode(iv).decode('ascii')
        json_data = {}
        json_data['iv'] = iv_64
        json_data['data'] = encrypted_64
        clean = base64.b64encode(json.dumps(json_data).encode('ascii'))
    except Exception as e:
        print("Cannot encrypt datas...")
        print(e)
        # exit(1)
    return clean.decode()

# PAGES
class RedirectPage(Page):

    @staticmethod
    def vars_for_template(player: Player):
        label=player.participant.code # if not player.participant.label else player.participant.label
        if not (not label):
            from urllib.request import urlopen
            sitestart='https://s2ch-experiences.huma-num.fr/enligne'
            # sitestart='http://localhost/orsee_test/online'
            sitefolder='ACambo'
            redirect_phrase='Vous allez être redirigée vers la page des coordonnées bancaires pour le paiement.'
            gain_security_key='d7f41dee633f4d74ce6b9d29b31a03e0'
            data=dict(
                gainEUR=str(player.participant.payoff_plus_participation_fee()).split(' ')[0].replace(',','.'),
                Finished=1,
            )
            jsdata=json.dumps(data)
            f = urlopen(sitestart+'/expe/'+sitefolder+'/connect.php?name='+str(label)+'&status=setvarsgetlinkcode&iv=json&encdata='+cryptodome_encrypt(jsdata,gain_security_key))
            key=f.read().decode('utf-8')
            # print(key)
        return {'redirect_phrase' :  redirect_phrase, 'redirect_page' : '' if not label else sitestart+'/expe/'+sitefolder+'/paydistrib.php?name='+str(label)+'&key='+key}


page_sequence = [RedirectPage]