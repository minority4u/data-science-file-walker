from app.IO import FileWalker
from app.Files import Wavefile, JsonFile, Dicomfile
from app.Setup import Console_and_file_logger
from app.Singelton_stats import *
from argparse import ArgumentParser
import yaml


def main(params):

    start_time = time()

    # fw = FileWalker(Wavefile, params["dir_to_src"], params["dir_to_dest"])
    # fw = FileWalker(JsonFile, params["dir_to_src"], params["dir_to_dest"])
    #log_wave_statistics()

    fw = FileWalker(Dicomfile, params["dir_to_src"], params["dir_to_dest"], static_destination=False)

    log_stats()


    logging.info('FileWalker finished after {:0.3f} seconds'.format(time() - start_time))


if __name__ == '__main__':

    # Define argument parser
    parser = ArgumentParser()

    # define arguments and default values to parse
    parser.add_argument("--config", "-c", help="Define the path to config.yml", default="config.yml", required=False)

    args = parser.parse_args()

    # Make sure the config exists
    assert os.path.exists(args.config), "Config does not exist!, Please create a config.yml in root or set the path with --config."

    # Load config
    params = yaml.load(open(args.config, "r"))

    # Make sure that source and destination are set
    assert {"dir_to_src", "dir_to_dest"} <= set(params.keys()), "Configuration is incomplete! Please define dir_to_src and dir_to_dest in config.yml"

    # Make sure source folder exists
    assert os.path.exists(params["dir_to_src"]), "Path to src {} does not exist!".format(params["dir_to_src"])

    # define a central logger
    Console_and_file_logger('FileWalker')

    # start the script
    main(params)
