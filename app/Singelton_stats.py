import logging
import numpy as np

# Modul treated as Singelton to summarize all statistics in one file

Wav_Files = 0
Total_duration = 0
Min_duration = 10
Max_duration = 0
Mean_file_duration = 0
Min_amplitude= 0
Max_amplitude = 0
Text_Files = 0
Total_words = 0
Mean_words = 0
Total_characters = 0
Distinct = set()
Distinct_words = 0

## helpers
duration_list = []

def log_statistics():
    """
    log the FileWalker data to console and file
    :return:
    """
    logging.info('Wave-Files: {}'.format(Wav_Files))
    logging.info('Total characters: {}'.format(Total_characters))
    logging.info('Total duration: {}'.format(Total_duration))
    logging.info('Min duration: {}'.format(Min_duration))
    logging.info('Max duration: {}'.format(Max_duration))
    logging.info('Mean file duration: {}'.format(Mean_file_duration))
    logging.info('Median file duration: {}'.format(np.median(np.array(duration_list))))
    logging.info('Min amplitude: {}'.format(Min_amplitude))
    logging.info('Max amplitude: {}'.format(Max_amplitude))
    logging.info('Text-Files: {}'.format(Text_Files))
    logging.info('Total Words: {}'.format(Total_words))
    logging.info('Mean Words: {}'.format(Mean_words))
    logging.info('Number of distincts words: {}'.format(Distinct_words))
    logging.debug('Distincts words: {}'.format(Distinct))

