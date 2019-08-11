# 8-stage-pipeline-simulator
8 stage pipeline simulation for MIPS 64 instructions in python

**Structure.py** contains the code for the strcuture of the pipeline. It contains classes for memory and cache and functions describing how to read and write to them

**stages.py** contains all the 8 stages functions and registers operating between these stages. It also contains function for preprocessing of the code file that the user will give.

**functions.py** contains all important helper functions such as bits to int, int to bits, etc

**code.txt** contains a sample code that our pipeline simulator can execute

**helper_text_files** contains regsiter files and memory files that depicts the current states of memory and registers.
