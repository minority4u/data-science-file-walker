from time import time
from app.Singelton_stats import *
from app.Files import Wavefile, JsonFile
from app.Setup import *


class FileWalker:
    open_files = []

    def __init__(self, file_wrapper, src_dir='./', dest_dir='', static_destination=False):
        """
        Calls the recursive file walker and runs the action method on each found object
        If no destination is given all transformed files will be stored within the folder 'transformed'
        :param src_dir:
        :param dest_dir:
        :return:
        """
        self.file_wrapper = file_wrapper
        self.static_destination = static_destination

        if static_destination:
            self.destination = dest_dir

        self._recursive_file_action(src_dir, dest_dir)

    def perform_action(self, current_src_dir='./', current_dest_dir=''):
        """
        Calls the recursive file walker and runs the action method on each found object
        If no destination is given all transformed files will be stored within the folder 'transformed'
        :param current_src_dir:
        :param current_dest_dir:
        :return:
        """
        if current_dest_dir == '':
            current_dest_dir = './transformed' + current_src_dir

        self._recursive_file_action(current_src_dir, current_dest_dir)

    def _recursive_file_action(self, current_src_dir, current_dest_dir):
        """
        Search recursively for the given file_typ in every sub-folder
        and performs the action method on each found file
        :param current_src_dir:
        :param current_dest_dir:
        :return:
        """
        t1 = time()
        logging.info('Current src directory: {0}'.format(current_src_dir))
        logging.info('Current dest directory: {0}'.format(current_dest_dir))

        # static destination-folder
        if self.static_destination:
            current_dest_dir = self.destination

        # for every file in this sub-folder
        for filename in os.listdir(current_src_dir):
            # perform action only on the given file ending
            if filename.endswith(self.file_wrapper.file_typ):
                # load the file
                try:
                    wrapped_file = self.file_wrapper(current_src_dir, filename, current_dest_dir)
                    # perform the action method defined in the file_wrapper class
                    # save the new wave file to the destination folder defined in settings.DIR_TO_DEST
                    self.open_files.append(wrapped_file.action())
                except Exception as e:
                    logging.error('Error with file: {} in directory: {}'.format(filename, current_src_dir))
                    logging.error(e)

            # further sub-directories found, recursively start file action for this folder
            elif os.path.isdir(os.path.join(current_src_dir, filename)):
                self._recursive_file_action(os.path.join(current_src_dir, filename),
                                            os.path.join(current_dest_dir, filename))

            # ignore all other files
            else:
                pass
                # logging.info('Skip file {} '.format(os.path.join(current_src_dir, filename)))

        logging.info('Action performed in sub-directory {} done in {:0.3f}s'.format(current_src_dir, time() - t1))
        logging.info('Action performed on {} files'.format(len(self.open_files)))

    def log_stats(self):
        """
        Log all statistics submitted in files
        This is a very generic statistic log
        :return:
        """
        if self.open_files:
            for idx, file in enumerate(self.open_files):
                logging.info('File: {}, {}'.format(idx, file.stats))
        else:
            logging.info('No files captured, maybe the action method from the file walker doesnt return self')



def test_jsonfiles():
    fw = FileWalker(Wavefile)
    fw.perform_action("./new_data/", "./dest_data/")
    log_wave_statistics()


def test_jsonfiles():
    fw = FileWalker(JsonFile)
    fw.perform_action("./new_data/", "./dest_data/")
    log_wave_statistics()


if __name__ == '__main__':
    logger = Console_and_file_logger(os.path.basename(__file__), "./dest_data/")
    # test_jsonfiles()
    test_jsonfiles()
