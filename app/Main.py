from app.IO import FileWalker
from app.Files import Wavefile, JsonFile, Dicomfile
from app.Setup import *
from app.Singelton_stats import *
from argparse import ArgumentParser
import yaml


def main(params):


    start_time = time()

    # fw = FileWalker(Wavefile)
    # fw.recursive_file_action(params["dir_to_src"], params["dir_to_dest"])
    #
    # fw = FileWalker(JsonFile)
    # fw.recursive_file_action(params["dir_to_src"], params["dir_to_dest"])

    fw = FileWalker(Dicomfile)
    fw.recursive_file_action(params["dir_to_src"], params["dir_to_dest"])

    #log_statistics()
    logging.info('FileWalker finished after {:0.3f} seconds'.format(time() - start_time))


if __name__ == '__main__':
    # define a central logger
    logger = Console_and_file_logger('FileWalker')

    # Define argument parser
    parser = ArgumentParser()
    cwd = os.getcwd()
    print(cwd)

    parser.add_argument("--src", help="Define a data source directory", default="./")
    parser.add_argument("--dest", help="Define a data destination directory", default="./transformed/")
    parser.add_argument("--config", "-c", help="Define the path to config.yml", default="config.yml", required=False)
    args = parser.parse_args()

    # make sure the config exists
    assert os.path.exists(args.config), "Config does not exist!"

    # load config
    params = yaml.load(open(args.config, "r"))
    assert {"dir_to_src", "dir_to_dest"} <= set(params.keys()), "Configuration is incomplete!"

    # Assertions
    assert os.path.exists(params["dir_to_src"]), "Path to src {} does not exist!".format(params["dir_to_src"])


    # start the script
    main(params)
