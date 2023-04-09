# Convert .z80 files to Micro-Professor MPF-1 files

## z80_to_mpf.py
### This is a Python script that takes a .z80 file as an argument and creates two output files ...
* .hex for use with H.M. Pragt's MPF1 emulator (https://www.heinpragt.com/english/software_development/MPF1_emulator.html)
* .wav for loading the file into a real Micro-Professor using the cassette input

## Installation
```
git clone https://github.com/dadecoza/z80-to-mpf.git
cd z80-to-mpf
pip3 install --user -r requirements.txt
```

## Usage example
I have included the helpus.asm example program (the "hello world" of MPF-1) and I'm using z80-asm (http://wwwhomes.uni-bielefeld.de/achim/z80-asm.html) as my assembler.

### Assemble the .asm file using z80-asm ...
```
z80-asm helpus.asm 1800:helpus.z80 
```
Note: The 1800 is the memory address in hex where the program will be loaded into the MPF-1.

### Creating the .hex and .wav files
```
python3 z80_to_mpf.py helpus.z80
```
Output:
```
Loading helpus.z80 ...
Creating Intel Hex file ...
Creating WAV file ...
All done!
```

## Loading the .hex file
In the MPF-1 emulator select "File" from the top left and then "Open hex file", then select the "helpus.hex" file.

On the emulator interface click \[ADDR\] and then enter \[1\]\[8\]\[0\]\[0\], and click \[GO\].

"HELP US" should now be displayed on the 7-segment displays.


## Loading the .wav file

You will require an audio cable with a 3.5mm stereo plug on one end, and a 3.5mm mono plug on the other.

You only need to connect one channel of the stereo plug.

Connect the stereo end of the cable to your computer's audio out and the mono plug to the MPF-1 "EAR" jack.

On the MPF-1 press the \[TAPE RD\] button followed by the file name \[1\]\[2\]\[3\]\[4\] and then press \[GO\].

On your computer open the "helpus.wav" file and press play.

After the file is done loading press the \[ADDR\] button followed by the start address \[1\]\[8\]\[0\]\[0\] and press the \[GO\] button.

"HELP US" should now be displayed on the 7-segment displays.






