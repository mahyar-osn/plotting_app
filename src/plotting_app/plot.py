import os
import argparse

import pandas as pd


class ProgramArguments(object):
    pass


class Plot(object):
    def __init__(self, input_file):
        self._input_file = input_file

        self._read_file()

    def get_input_file(self):
        return self._input_file

    def _read_file(self):
        pd.read_csv(self._input_file, sep=',', header=0)


def main():
    args = parse_args()
    if os.path.exists(args.input_file):
        input_file = args.input_file
        file_path, _ = os.path.split(args.input_file)
        file_name_path, image_format = os.path.splitext(args.input_file)
        file_name = file_name_path.split('\\')[-1]

        if args.plot_type is None:
            plot_type = 'scatter'
        else:
            plot_type = str(args.plot_type)

        save = False
        save_filename = None

        if args.export_plot:
            save = True
            save_filename = os.path.join(file_path, 'exported_plot.png')

        p = Plot(input_file)


def parse_args():
    parser = argparse.ArgumentParser(description="Physiological data plotting and visualization for NIH-SPARC MAPCore.")
    parser.add_argument("input_file", help="Location of the input data file. Currently only CSV (or related format) is"
                                           "supported")
    parser.add_argument("--plot_type", help="Type of plot e.g. scatter, bar chart, heatmap etc."
                                            "Options: \n"
                                            "\t scatter\n"
                                            "\t bar \n"
                                            "[default is scatter.]")
    parser.add_argument("--export_plot", help="Saves plot as an image file."
                                              "Location is the same as input file's location.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    main()
