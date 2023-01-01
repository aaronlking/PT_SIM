# Page-Table-Simulator

## Instructions to Run:
***Assuming Page Table state from PT_A.txt***
1. **Running Part A: ptsim**
    - Inputting one virtual address at a time via CLI.
        - `$ make ptsim`
        - `$ sh ptsim tests/PT_A.txt`
        - *Enter (one by one) virtual addresses to translate.*
        - *Crtl+D to terminate.*
    - Using I/O redirection to translate addresses from input file and diff the expected output.
        - `$ make ptsim`
        - `$ sh ptsim tests/PT_A.txt < tests/test_input1.txt > tests/actual_output/ptsim_PT_A_output1.out`
        - `$ diff tests/expected_output/ptsim_PT_A_output1.txt tests/actual_output/ptsim_PT_A_output1.out`
        - *No Diff (hopefully)*
2. **Running Part B: ptsim-clock**
    - Inputting one virtual address at a time via CLI.
        - `$ make ptsim-clock`
        - `$ sh ptsim-clock tests/PT_A.txt`
        - *Enter (one by one) virtual addresses to translate.*
        - *Crtl+D to terminate.*
    - Using I/O redirection to translate addresses from input file and diff the expected output.
        - `$ make ptsim`
        - `$ sh ptsim-clock tests/PT_A.txt < tests/test_input1.txt > tests/actual_output/ptsim_clock_PT_A_output1.out`
        - `$ diff tests/expected_output/ptsim_clock_PT_A_output1.txt tests/actual_output/ptsim_clock_PT_A_output1.out`
        - *No Diff (hopefully)*
3. **Quick Testing of Differences (Hard Coded for specific I/O).**
    - `$ make check`
    - *No Diff (hopefully)*

## Contributors:
- [Aaron King](https://github.com/aaronlking)
- [Gary Singh](https://github.com/Gary-Git)
- [Owen Mastropietro](https://github.com/OwenMastropietro)

## TODO:
- Have the page table as a dictionary {key:"101", value:[V, P, F, U]}.

## Gondree's README Content.
The files `pt-sim.sh` and `pt-sim-clock.sh` are wrapper files you should modify to call your executables.

You should add Makefile logic so that your program can be run with commands like:

    $ make ptsim
    $ make ptsim-clock
    $ sh ptsim test/aPageTableFile < test/anInputFile
    $ sh ptsim-clock test/aPageTableFile < test/anInputFile
