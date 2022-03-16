"""Extract data on near-Earth objects and close approaches from CSV and JSON
files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
commandline, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
from importlib.resources import contents
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
    objects.
    :return: A collection of `NearEarthObject`s.
    """
    # create a list to hold neos that will be extracted from the file
    neos = []

    # opens the file and appends each neo to the list created
    with open(neo_csv_path, 'r') as csvF:
        reader = csv.DictReader(csvF)
        for elem in reader:
            neo = NearEarthObject(**elem)
            neos.append(neo)

    return neos


load_neos("./data/neos.csv")


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about
    close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # create a list to hold approaches that will be extracted from the file
    cad = []
    # opens the file and appends each approach to the list created
    with open(cad_json_path, 'r') as jsonF:
        contents = json.load(jsonF)
        for value in contents["data"]:
            ca = CloseApproach(**dict(zip(contents["fields"], value)))
            cad.append(ca)
    return cad


load_approaches("./data/cad.json")
