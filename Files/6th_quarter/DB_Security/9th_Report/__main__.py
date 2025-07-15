import os, argparse, platform
from code import AC09

os.system('cls') if platform.system() == 'Windows' else os.system('clear')

# ===== Configs Default
parser = argparse.ArgumentParser()
parser.add_argument('--formaEjecucion', type=str, default='poner y quitar', help='Indica que procesos tiene que seguir el script. Opciones disponibles son: "poner","quitar","poner y quitar".')
parser.add_argument('--userSQL',        type=str, default='postgres',       help='Indica el usuario con el que se va a conectar al server. El valor default es: postgres')
parser.add_argument('--pswdSQL',        type=str, default='postgres',       help='Indica la contraseña con la que se va a conectar al server. El valor default es: postgres')
parser.add_argument('--dataSQL',        type=str, default='postgres',       help='Indica el nombre de la base de datos a la que se va a conectar al server. El valor default es: postgres')
parser.add_argument('--hostSQL',        type=str, default='localhost',      help='Indica el host al que se va a conectar como server. El valor default es: localhost')
parser.add_argument('--portSQL',        type=str, default='5432',           help='Indica el puerto del host al que se va a conectar. El valor default es: 5432')

args = parser.parse_args()

# ===== Ejecución de código AC09
report = AC09(
    forma_ejecucion = args.formaEjecucion,
    user            = args.userSQL,
    password        = args.pswdSQL,
    db_name         = args.dataSQL,
    host            = args.hostSQL,
    port            = int(args.portSQL)
)
report.main()

