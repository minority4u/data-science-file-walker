# FileWalker with wave-file wrapper v.02
This project consists of two small modules, the FileWalker and the FileWrapper.

The FileWalker will search for all files (defined by the initiated FileWrapper) within "dir_to_src".
Afterwards it performs the file_wrappers' action method on each file.
All changed files will be stored within "dir_to_dest"

The FileWrapper class specifies the file-typ and the action method that should be performed.
To make things easier a base FileWrapper-class is defines which provides some simple helper functions.

New FileWrapper could be inherited from BaseFile. Methods you need to overwrite for your own Wrapper-Class:

def action(self):, def __load_file__(self, filename):



## Project structure:

### Main 
Callable entry point for this project, currently it does not trim, just describe (commented out)
### Setup 
Small central setup file with predefined logger
### IO
Defines the recursive FileWalker
### Files
Specifies the BaseFileWrapper and all implemented FileWrapper with given action method
### Singelton_stats
Statistics Module which is used by the FileWrappers to summarize the statistcs



# Implemented FileWrapper

Actually there is one BaseFileWrapper with some helper functions to inherit from.
For the text2speech projekt two subclasses are implemented the WaveFileWrapper and the JSOnFileWrapper.

The dataset description log contains the following metrics:

Wave-Files: 10055
Total characters: 2254080
Total duration: 70591.62550000008
Min duration: 1.1598125
Max duration: 17.4698125
Mean file duration: 7.020549527598218
Median file duration: 6.9198125
Min amplitude: -32768
Max amplitude: 32767
Text-Files: 20128
Total Words: 372762
Mean Words: 18.519574721780604
Number of distincts words: 44710


## WaveFileWrapper
Provides to simple functionalities encapsulated by the action method

1. Describe()
Analyze a wave-file and write the statistics into the statistics module to log them afterwards

2. trim()
Detects the starting bin of a speaking voice within a wav file
by comparing the rolling average (window size 4) difference between two consecutive bins.
This script trims silent space at the beginning and the end of a wav file.

### Parameters for the WaveFileWrapper
The WaveFileWrapper has some parameter to change its behaviour. 
It provides different buffer and delta parameters for trimming the starting point and the end.
This is because the voice raises faster at the beginning of an example, than at the end.

START_DELTA defines the necessary difference between two bins to recognize the beginning

END_DELTA defines the necessary difference between two bins to recognize the end

START_BUFFER defines the number of bins to the left of the detected starting bin
and include this buffer to the trimmed files to avoid clipped voices.

END_BUFFER defines the number of bins to the right of the detected ending bin
and include this buffer to the trimmed files to avoid clipped voices.

## JSONFileWrapper
Reads the clean string of the a Metadata_mls.json files.
Functionalities:

1. Describe()
Calculates all text related statistics from the given json-file and writes it into the statistics file.

# How to run
1. Clone
2. Install requirements from requirements.txt
3. Define the path to your source folder in config.yml
4. Define the destination path to store the modified wav-files in config.yml
5. Run Main.py
