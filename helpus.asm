        ORG     0x1800
        LD      IX, HELP
DISP    CALL    SCAN
        CP      0x13
        JR      NZ, DISP
        HALT
        ORG     0x1820
HELP    DEFB    0xae        ; 'S'
        DEFB    0xb5        ; 'U'
        DEFB    0x1f        ; 'P'
        DEFB    0x85        ; 'L'
        DEFB    0x8f        ; 'E'
        DEFB    0x37        ; 'H'
SCAN    EQU 0x5fe

