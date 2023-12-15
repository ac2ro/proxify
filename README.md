
# Proxify

Proxify is a Simple DLL proxy generator written in python. It utilizes ```pefile``` to parse the EAT out of DLLs and loop through the exports and get the name and ordinal for each export for pragma linker comments generation.



## Guide
To generate DLL proxies with proxify clone the repository and ``cd`` into it. run ```python proxify.py --help``` to see the summarized help log.
## Usage/Examples

```batch
python proxify.py --dll C:\Windows\System32\advapi32.dll --output main.c --payload calc.bin
```
This generates a DLL proxy C source file for ``advapi32.dll`` which loads ``calc.bin`` shellcode file upon being loaded.

```batch
python proxify.py --dll C:\Windows\System32\ntdll.dll --output main.c --payload calc.bin
```
This also generates a DLL proxy C source file but for ``ntdll.dll``. Keep in mind that the larger the dlls , the larger the source file will be.