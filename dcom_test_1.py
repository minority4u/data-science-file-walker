import logging
from app.Files import Dicomfile
from app.IO import FileWalker
from app.Setup import Console_and_file_logger


def move_dicom():
    """
    demo usage of the file walker
    :return:
    """

    class MyDicomfile(Dicomfile):
        """
        you need to implement:
        file_type
        def __init__(self, dir_name='./', filename='test.dcm', destination='./dest'):
        action(self):

        important, return the file for later statistics
        """
        file_type = '.dcm'

        def __init__(self, dir_name='./', filename='test.dcm', destination='./dest'):
            super(MyDicomfile, self).__init__(dir_name, filename, destination)
            self.stats['filetype'] = self.__class__.file_type

        def action(self):
            logging.info('action performed')
            return self

    fw = FileWalker(MyDicomfile, 'testdata/input/multifile', 'testdata/output/test123')
    fw.log_stats()


if __name__ == '__main__':
    logger = Console_and_file_logger('my_test_1')
    move_dicom()