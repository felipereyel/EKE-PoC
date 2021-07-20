import base64
import secrets

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

from tinyec import registry
from tinyec.ec import Point

BS = 16

class AESCipher:
    def __init__(self, intKey):
        self.key = intKey.to_bytes(32, 'big')

    @property
    def keyStr(self):
        return base64.b64encode(self.key).decode()

    def encrypt(self, msg):
        raw = str.encode(msg)
        raw = pad(raw, BS)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("ascii")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:BS]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt( enc[BS:] ), BS).decode()

curve = registry.get_curve('secp256r1')

class EKE:
    def __init__(self, privKey, otherPub, curve=curve):
        self.curve = curve
        self.privKey = privKey
        self.otherPub = Point(self.curve, otherPub["x"], otherPub["y"])

    def startExchange(self):
        mySessionSecret = secrets.randbelow(self.curve.field.n)
        toOther = (self.privKey + mySessionSecret) * self.otherPub

        self.mySelfPartialShared = mySessionSecret * self.curve.g
        return toOther.x, toOther.y

    def endExchange(self, receivedX, receivedY):
        received = Point(self.curve, receivedX, receivedY)

        privKeyInv = pow(self.privKey, -1, self.curve.field.n)
        myPartialShared =  (received * privKeyInv) - self.otherPub
        shared = self.mySelfPartialShared + myPartialShared

        self.cipher = AESCipher(shared.x)
        return shared.x
