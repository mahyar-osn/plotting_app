import sys
import os
import argparse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class ProgramArguments(object):
    pass


class Plot(object):
    def __init__(self, input_file, **kwargs):
        self._input_file = input_file
        self._df = None

        if kwargs:
            if 'file_name' in kwargs.keys():
                self._file_name = kwargs['file_name']
            if 'save' in kwargs.keys():
                self._save = kwargs['save']
            if 'save_filename' in kwargs.keys():
                self._save_filename = kwargs['save_filename']

        self._read_file()
        # self._plot_timeseries()
        self._plot_timeseries_qt()

        print('done')

    def get_input_file(self):
        return self._input_file

    def get_data_frame(self):
        return self._df

    def _read_file(self):
        sys.stdout.write('Reading {}. This may take some time.'.format(self._file_name) + '\n')
        self._df = pd.read_csv(self._input_file, sep=',', header=0, usecols=[0, 1, 2])

    def _restructure_data(self):
        if self._df is not None:
            self._df["time"] = self._df.index
            self._df = self._df[:50000]
            self._df = pd.melt(self._df, ["time"])

    def _plot_timeseries_qt(self):
        app = QtGui.QApplication([])
        view = pg.GraphicsView()
        l = pg.GraphicsLayout(border=(100, 100, 100))
        view.setCentralItem(l)
        view.show()
        view.setWindowTitle('Functional recordings from the pig intrinsic cardiac nervous system (ICN)')
        view.resize(800, 600)

        text = """
                In this dataset, pigs were investigated for intrinsic cardiac nervous system (ICN)
                recoding via cardiovascular output monitoring after cervical vagi stimulation.
                """

        l.addLabel(text, row=1, col=1)
        l.nextRow()

        p1 = l.addPlot(row=2, col=1, title="ECG")
        l.nextRow()
        p2 = l.addPlot(row=3, col=1, title="LVP")
        p3 = l.addPlot(row=4, col=1, title="RAE")
        self._df["time"] = self._df.index
        self._df = self._df[:500000]
        p1.plot(self._df["time"], self._df[self._df.keys()[0]])
        p2.plot(self._df["time"], self._df[self._df.keys()[1]])
        p3.plot(self._df["time"], self._df[self._df.keys()[2]])

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def _plot_timeseries(self):
        self._restructure_data()
        ax = sns.lineplot(x="time", y="value", hue="variable",
                          estimator=None, lw=1,
                          data=self._df)
        plt.show()


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

        p = Plot(input_file, file_name=file_name, save=save, save_filename=save_filename)


def parse_args():
    parser = argparse.ArgumentParser(description="Physiological data plotting and visualization for NIH-SPARC MAPCore.")
    parser.add_argument("input_file", help="Location of the input data file. Currently only CSV (or related format) is"
                                           "supported")
    parser.add_argument("--plot_type", help="Type of plot e.g. scatter, bar chart, heatmap etc."
                                            "Options: \n"
                                            "\t scatter\n"
                                            "\t bar \n"
                                            "\t time-series \n"
                                            "[default is scatter.]")
    parser.add_argument("--export_plot", help="Saves plot as an image file."
                                              "Location is the same as input file's location.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    main()
