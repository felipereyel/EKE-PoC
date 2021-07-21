import argparse, sys, json

def init():

    parser = argparse.ArgumentParser()
    parser.add_argument('--usuario', '-u', dest='user', help='Seu usuario', required=True)
    parser.add_argument('--destinatario', '-d', dest='dest', help='Usuario com que se quer conectar', required=True)
    parser.add_argument('--debug', dest='debug', help='Mostrar Debug Prints', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if args.user == args.dest:
        sys.exit("Destinatario e usuario nao podem ser os mesmos")

    f = open('public.json')
    publicRegister = json.load(f)

    dest, *_ = [n for n in publicRegister if n["user"] == args.dest]
    if not dest:
        sys.exit("Destinatario nao achado")

    f = open(f'{args.user}.private.json')
    user = json.load(f)

    userCheck, *_ = [n for n in publicRegister if n["user"] == args.user]
    if not userCheck:
        sys.exit("Usuario nao achado")

    return dest, user, args.debug