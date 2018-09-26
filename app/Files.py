from scipy.io import wavfile
import json

import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import logging
import os
import app.Singelton_stats as stats
import SimpleITK as sitk
from app.helper.Dicomhelper import myshow, myshow3d


class Basefile:
    file_typ = '.basefile'

    def __init__(self, dir_name='./', filename='test.wav', destination='./dest'):
        """
        Opens a file from the given directory
        :param dir_name:
        :param filename:
        :param destination:
        """
        logging.debug('Trying to open: {0}'.format(os.path.join(dir_name, filename)))
        #logging.debug('Current Destination path: {0}'.format(os.path.join(destination, filename)))
        self.dir = dir_name
        self.filename = filename
        self.destination = destination

    def action(self):
        print('{} method not implemented'.format(self.action.__name__))

    def __load_file__(self, filename):
        print('{} method not implemented'.format(self.__load_file__.__name__))

    def save(self):
        print('{} method not implemented'.format(self.save.__name__))

    def describe(self):
        print('{} method not implemented'.format(self.describe.__name__))

    def update(self, dir):
        """
        Update the directory
        :param dir:
        :return:
        """
        self.dir = dir

    def __ensure_dir__(self, file_path):
        """
        Make sure a directory exists or create it
        :param file_path:
        :return:
        """
        if not os.path.exists(file_path):
            logging.debug('Creating directory {}'.format(file_path))
            os.makedirs(file_path)

    def __save_plot__(self, fig, path, filename=''):
        """
        Saves an matplotlib figure to the given path + filename
        If the figure exists, ad a number at the end and increase it
        as long as there is already an image with this name
        :param fig:
        :param path:
        :param filename:
        :return:
        """
        logging.debug('Trying to save to {0}'.format(path))
        self.__ensure_dir__(path)
        i = 0
        while True:
            i += 1
            newname = '{}{:d}.png'.format(filename + '_', i)
            if os.path.exists(os.path.join(path , newname)):
                continue
            fig.savefig(os.path.join(path , newname))
            break
        logging.debug('Image saved: {}'.format(os.path.join(path, newname)))
        # free memory, close fig
        plt.close(fig)


class Dicomfile(Basefile):
    file_typ = '.dcm'

    def __init__(self, dir_name='./', filename='test.dcm', destination='./dest'):
        """
        Opens a dicom file from the given directory
        :param dir_name:
        :param filename:
        :param destination:
        """
        super(Dicomfile, self).__init__(dir_name, filename, destination)
        self.img = self.__load_file__(os.path.join(dir_name, filename))

    def action(self):
        """
        Single entry point for the FileWalker
        Call here all functions you would like to perform
        :return:
        """


        self.describe()

        if self.stats['size'] == (192, 168, 1):
            logging.debug('saving')
            self.save()

        #self.__print3d__()
        #self.__segmentation_test1__()
        #self.save()

    def __load_file__(self, filename):
        """
        This function uses the simpleITK library for dicom image loading
        :param filename:
        :return:
        """
        return sitk.ReadImage(filename)

    def save(self):
        """
        Use simpleITK to write the current dicom file to disk
        :return:
        """
        self.__ensure_dir__(self.destination)
        sitk.WriteImage(self.img, os.path.join(self.destination, self.filename))

    def describe(self):
        """
        # Describe a dicom image
        # writes all statistics to the singelton file for later printing and logging
        :return:
        """
        self.stats = {}
        image = self.img

        # Get all Metadata for a dicom file
        # metadata = {}
        # for key in image.GetMetaDataKeys():
        #     metadata[key] = image.GetMetaData(key)
        # logging.info(metadata)
        # stats.files.append(metadata)

        # create a dictionary with all important file meta data
        self.stats['filetyp'] = self.file_typ
        self.stats['file'] = self.filename
        self.stats['src_path'] = self.dir
        self.stats['dimension'] = image.GetDimension()
        self.stats['size'] = image.GetSize()
        self.stats['origin'] = image.GetOrigin()
        self.stats['spacing'] = image.GetSpacing()

        # append the file statistics to the stats singelton for later usage
        stats.files.append(self.stats)

    def __print3d__(self):
        """
        Creates an matplotlib figure and save it to disk
        :return:
        """
        # plt.imshow(sitk.GetArrayViewFromImage(self.img[:,:,0]))
        # plt.title(self.filename)
        # self.__save_plot__(plt.gcf(), self.destination, self.filename)


        fig = myshow3d(img=self.img, title=self.filename)
        self.__save_plot__(fig, self.destination, self.filename)

    def __segmentation_test1__(self):
        """
        Testfunction for segmentations
        :return:
        """
        # To visualize the labels image in RGB with needs a image with 0-255 range
        img_255 = sitk.Cast(sitk.RescaleIntensity(self.img), sitk.sitkUInt8)

        # Threshold segmentation
        #seg = self.img > 100
        #fig = myshow(sitk.LabelOverlay(img_255, seg), "Basic Thresholding")
        # self.__save_plot__(fig, self.destination, self.filename)

        # histogram based segmentation
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(0)
        otsu_filter.SetOutsideValue(1)
        seg = otsu_filter.Execute(self.img)
        fig = myshow(sitk.LabelOverlay(img_255, seg), "Otsu Thresholding")
        self.__save_plot__(fig, self.destination, self.filename)

        # Region Growing Segmentation
        seed = (132, 142, 96)
        seg = sitk.Image(self.img.GetSize(), sitk.sitkUInt8)
        seg.CopyInformation(self.img)
        seg = sitk.ConnectedThreshold(self.img, seedList=[seed], lower=100, upper=190)
        myshow(sitk.LabelOverlay(img_255, seg), "Connected Threshold")



class Wavefile(Basefile):
    file_typ = '.wav'
    # WavFile settings
    # START_DELTA defines the necessary difference between two bins to recognize the beginning
    # END_DELTA defines the necessary difference between two bins to recognize the end
    # START_BUFFER defines the number of bins to the left of the detected starting bin
    # and include this buffer to the trimmed files to avoid clipped voices.
    # END_BUFFER defines the number of bins to the right of the detected ending bin
    # and include this buffer to the trimmed files to avoid clipped voices.
    START_DELTA = 1000
    END_DELTA = 500
    START_BUFFER = 1000
    END_BUFFER = 2000
    MOV_AVG_WINDOW_SIZE = 4

    def __load_file__(self, filename):
        """
        Loads a wavfile from a given path
        This method encapsulates the used library
        :param filename:
        :return:
        """
        return wavfile.read(filename)

    def __init__(self, dir_name='./', filename='test.wav', destination='./dest'):
        """
        Initialize and open a wav file from the given directory
        :param dir_name:
        :param filename:
        """
        super(Wavefile, self).__init__(dir_name, filename, destination)
        self.fs, self.data = self.__load_file__(os.path.join(dir_name, filename))

    def action(self, destination='./transformed/'):
        """
        Central entry point for this file
        The FileWalker will perform thi method on each found wave-file
        :param destination:
        :return:
        """
        # describe the untrimmed wave-file
        # self.describe()
        # self.plot_and_save_wav_file()
        # find silent space at the beginning, trim it and save the new wave-file
        # self.trim()
        # describe the trimmed wave-file
        self.describe()
        # self.plot_and_save_wav_file()

    def save(self):
        """
        Saves the wav file
        :return:
        """
        self.__ensure_dir__(self.dir)
        wavfile.write(os.path.join(self.dir, self.filename), self.fs, self.data)

    def describe(self):
        """
        Define some helpful metrics for this file
        :return:
        """

        audio = self.data
        frame_rate = self.fs
        signal = np.fromstring(audio, 'Int16')
        length = len(signal) / frame_rate

        # write our statistics into the singelton stats-modul for later logging
        stats.Wav_Files += 1
        stats.Total_duration += length
        stats.Min_duration = min(stats.Min_duration, length)
        stats.Max_duration = max(stats.Max_duration, length)
        stats.Max_amplitude = max(stats.Max_amplitude, signal.max())
        stats.Min_amplitude = min(stats.Min_amplitude, signal.min())
        stats.Mean_file_duration = stats.Total_duration / stats.Wav_Files
        stats.duration_list.append(length)

        logging.debug('Current length = {} seconds.'.format(length))
        logging.debug('Current max = {}'.format(signal.max()))
        logging.debug('Current min = {}'.format(signal.min()))

    def trim(self):
        """
        Trim the current wav file
        save it afterwards to dir
        :param dir:
        :return:
        """
        self.data = self.__trim_file__(self.data)
        logging.debug('File trimmed')
        self.dir = self.destination
        self.save()

    def plot_and_save_wav_file(self):
        """
        works with mono files
        :param input_data:
        :return:
        """

        signal = np.fromstring(self.data, 'Int16')
        # create a Time Vector spaced linearly with the size of the audio file
        time = np.linspace(0, len(signal) / self.fs, num=len(signal))
        plt.figure()
        plt.plot(time, signal)
        # label the axes
        plt.ylabel("Amplitude")
        plt.xlabel("Time in sec")
        # set the title
        plt.title(self.filename)
        self.__save_plot__(plt.gcf(), self.destination, self.filename)

    def __trim_file__(self, untrimmed_file):
        """
        Internal trimming function
        :param untrimmed_file:
        :return trimmed_file:
        """
        # get the mov_avg for the given array, window size = 4 buckets
        mov_avg = self.__get_mov_avg__(arr=untrimmed_file)

        start_index = self.__get_start_index__(mov_avg)
        logging.debug('Start index = {0}'.format(start_index))
        logging.debug(untrimmed_file[start_index - 1:start_index + 1])

        end_index = self.__get_end_index__(mov_avg)
        logging.debug('End index = {0}'.format(end_index))
        logging.debug(untrimmed_file[end_index - 1:end_index + 1])

        return np.asarray(untrimmed_file[start_index:end_index], dtype=np.int16)

    def __get_mov_avg__(self, arr, window_size=MOV_AVG_WINDOW_SIZE):
        """
        Calculates the moving avg for a given array
        :param arr, window_size:
        :return moving_avg_arr:
        """
        return np.convolve(arr, np.ones((window_size,)) / window_size, mode='valid')

    def __get_start_index__(self, arr):
        """
        Returns the beginning of a speaking voice within a wav-file
        :param wave file data as arr:
        :return:
        """
        # initialize with the first bucket
        last_bucket = arr[0]

        # inner function which compares to bins within a wav file
        def is_significant_change(elem1, elem2):
            return (abs(elem1) - abs(elem2)) > self.START_DELTA

        # go through all bins in this wav file and compare t and t-1
        for idx, bucket in enumerate(arr):
            if is_significant_change(bucket, last_bucket):
                # avoid returning an index smaller than 0
                if idx - self.START_BUFFER < 0:
                    return 0
                else:
                    return idx - self.START_BUFFER
            else:
                last_bucket = bucket
        # if no significant change is noticeable, avoid returning None, keep wav file as it is
        return 0

    def __get_end_index__(self, arr):
        """
        Returns the end of a speaking voice within a wav-file
        :param wave file data as arr:
        :return ending index:
        """
        # initialize with the last bucket
        last_bucket = arr[-1]

        # inner function which compares to bins within a wav file
        def is_significant_change(elem1, elem2):
            return (abs(elem1) - abs(elem2)) > self.END_DELTA

        # go through all bins in reversed order and compare the wav file buckets t and t-1
        for idx, bucket in reversed(list(enumerate(arr))):
            if is_significant_change(bucket, last_bucket):
                # avoid returning an index smaller than 0
                if idx + self.END_BUFFER > arr.size:
                    return arr.size
                else:
                    return idx + self.END_BUFFER
            else:
                last_bucket = bucket
        # if no significant change is noticeable, avoid returning None, keep wav file as it is
        return arr.size


class JsonFile(Basefile):
    file_typ = '.json'

    def __init__(self, dir_name='./', filename='test.json', destination='./dest'):
        """
        Initialize and open a wav file from the given directory
        :param dir_name:
        :param filename:
        """
        super(JsonFile, self).__init__(dir_name, filename, destination)
        self.data = self.__load_file__(os.path.join(dir_name, filename))

    def action(self):
        self.describe()

    def describe(self):
        # from pprint import pprint
        # pprint(self.data)
        for file, text_json in self.data.items():
            # calc statistics
            sentence = self.__extract_str__(text_json)
            words = sentence.split()
            number_of_words = len(words)
            stats.Distinct |= set(words)
            stats.Distinct_words = len(stats.Distinct)
            stats.Total_words += number_of_words
            stats.Text_Files += 1
            stats.Total_characters += len(sentence)

        stats.Mean_words = stats.Total_words / stats.Text_Files

    def __extract_str__(self, json_snippet):
        used_text = 'clean'
        return json_snippet[used_text]

    def __load_file__(self, filename):
        with open(filename, encoding='utf-8', errors='ignore') as f:
            json_file = json.load(f)
            return json_file


def tests():
    dFile = Dicomfile(dir_name="testdata", filename="test.dcm", destination="destination/")


if __name__ == '__main__':
    from app.Setup import *

    # define a central logger
    logger = Console_and_file_logger('Files_tests')
    tests()
