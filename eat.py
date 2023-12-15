import pefile , argparse , os , sys 

from core.prompt import RavePrompt as prompt , Colors

ORANGE = Colors.ORANGE

END = Colors.END

parser = argparse.ArgumentParser (

    prog = 'EAT Viewer',

    description = 'Simple script to parse EAT out of a PE file.'

)


parser.add_argument('-f' , '--file' , help = 'Path to file to be parsed.')
parser.add_argument('-d' , '--detailed' , help = 'Shows you the ordinal of exported functions.')


arguments = parser.parse_args()


file_path = arguments.file
detailed = arguments.detailed


if not os.path.exists(file_path):

    prompt.print_min('File was not found.')

    sys.exit(0)


FILE = pefile.PE(file_path)


EAT = FILE.DIRECTORY_ENTRY_EXPORT.symbols

ROUTINE_COUNT = len (EAT)


for EXPORT in EAT:

    NAME = EXPORT.name


    if not NAME: continue

    NAME_DEC = NAME.decode()

    if detailed and detailed.lower() in ['y' , 'yes']:

        prompt.print_plus(f'{NAME_DEC} , {EXPORT.ordinal}')

    else:

        prompt.print_plus(NAME_DEC)



prompt.print_plus(f'Found {ORANGE}{ROUTINE_COUNT}{END} exported routines.')