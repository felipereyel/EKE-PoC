const { randomInt } = require("crypto");
const EC = require("elliptic").ec;
const ec = new EC("secp256k1");

///////////// Registration

/*Alice side*/
const AKey = ec.genKeyPair();

/*Bob side*/
const BKey = ec.genKeyPair();

///////////// Pre-exchange

/*Alice side*/
const ASecret = ec.genKeyPair();
const toB = BKey.getPublic().mul(ASecret.getPrivate().add(AKey.getPrivate()));

/*Bob side*/
const BSecret = ec.genKeyPair();
const toA = AKey.getPublic().mul(BSecret.getPrivate().add(BKey.getPrivate()));

///////////// Pos-exchange

/*Alice side*/
const APartialShared = toA
  .mul(AKey.getPrivate().invm(ec.n))
  .add(BKey.getPublic().neg());

const AShared = APartialShared.add(ASecret.getPublic());
console.log(AShared.getX().toJSON());

/*Bob side*/
const BPartialShared = toB
  .mul(BKey.getPrivate().invm(ec.n))
  .add(AKey.getPublic().neg());

const BShared = BPartialShared.add(BSecret.getPublic());
console.log(BShared.getX().toJSON());
