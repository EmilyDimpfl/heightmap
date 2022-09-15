#!/usr/bin/env python3

import csv
import re
from matplotlib import pyplot as plt
import numpy as np


def main():
    dist = []
    height = []

    # read in csv:
    with open('heightmap.csv') as file:
        iter_rows = csv.reader(file)
        for row in iter_rows:
            dist.append(float(row[0]))
            height.append(float(row[1]))

    # convert to numpy arrays for convenience:
    dist = np.array(dist)
    height = np.array(height)

    # calculate polynomial
    order = 25  # how many terms we want
    terms = np.polyfit(dist, height, order)
    f = np.poly1d(terms)

    # calculate values from our function:
    num_points = 1000
    dist_new = np.linspace(dist[0], dist[-1], num_points)
    height_new = f(dist_new)

    # plot our data sets:
    plt.plot(dist, height, dist_new, height_new)

    # label stuff:
    plt.xlabel("Distance Traveled (miles)")
    plt.ylabel("Elevation (feet)")
    plt.title("Jesse's Journey from Healdsburg to UCSB")

    # stuff for making graph pretty:
    tot_dist = dist.max() - dist.min()
    tot_height = height.max() - height.min()
    plt.xlim(dist.min() - tot_dist * 0.01, dist.max() + tot_dist * 0.01)
    plt.ylim(height.min() - tot_height * 0.01,
             height.max() + tot_height * 0.01)

    plt.show()

    def print_md_func(f: np.poly1d):
        """
        Prints a markdown version of the function we've computed.
        """
        output = ""
        # add each term to our output string:
        for index, coeff in enumerate(f.coefficients):
            # note: higher order polynomials come first in the list
            output += f"{'%.6g' % coeff}*x^{{{len(f.coefficients) - index - 1}}} + "

        # clean up:
        output = output.replace("+ -", "- ")
        # add markdown math formatting:
        output = f"${output}$"
        # change "1234e-56" to "1234*10^{-56}" (etc) for pretty printing
        output = re.sub("e(-?[\d]+)", "*10^{\g<1>}", output)
        # clean up the end of the string:
        output = re.sub("\*x\^\{0} \+ \$", "$", output)

        print(output)

    print_md_func(f)


if __name__ == "__main__":
    main()
