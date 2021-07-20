import secrets
from tinyec import registry
from tinyec.ec import Point
from Crypto.Cipher import AES

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

        self.key = shared.x
        return shared.x

    def crypt(self, msg):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(msg)
        return nonce, ciphertext, tag

    def decrypt(self, nonce, ciphermsg, tag):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphermsg)
        cipher.verify(tag)
        return plaintext
