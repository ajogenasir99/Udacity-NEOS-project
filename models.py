"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # get needed attibutes from variadic keyword parameters.
        designation = info.get('pdes')
        name = info.get('name')
        diameter = info.get('diameter')
        hazardous = info.get('pha')

        # handling potential edge cases for name and diameter arguments.

        if name == '':
            name = None
        if diameter == "":
            diameter = 'nan'

        # set class attributes from arguments extracted from the constructor.

        self.designation = designation
        self.name = name
        self.diameter = float(diameter)
        self.hazardous = bool(hazardous.lower() == 'y')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # create a fullname attribute using self.name and self.designation.
        # handle potential lack of name attribute.

        if self.name:
            full_name = f"{self.designation} {self.name}"
        else:
            full_name = f"{self.designation}"
        return full_name

    @property
    def isHazardous(self):
        #checks the value of hazardous 
        #and formats the __str__ differently depending on the result.
        if self.hazardous:
            return ""
        else:
            return " not"

    def __str__(self):
        """Return `str(self)`."""

        # returns human readable string representation using the class attributes.
        return f"{self.fullname} has a diameter of {self.diameter:.3f} km and is{self.isHazardous} potentially hazardous."


    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        
        # get the needed attributes from the variadic params and handle edge cases.
        designation = info.get('des')
        time = info.get('cd')
        distance = info.get('dist', "nan")
        velocity = info.get('v_rel', "nan")
        neo = info.get('neo', "UnNamed Close Approach")

        # set class attributes from arguments extracted from the constructor.

        self._designation = str(designation)
        # convert self.time to a datetime object
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # create a human readable representation self.time
        time_to_datetime = datetime_to_str(self.time)
        return time_to_datetime

    def __str__(self):
        """Return `str(self)`."""

        # returns human readable string representation using the class attributes
        # and the fullname attribute of the referenced neo
        return f"on {self.time_str} '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""

        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        # returns a dictionary with the relevant attributes for csv/json serialization


        if not self.neo.name:
            self.neo.name = 'None'
        return {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': {'designation': self.neo.designation,
                    'name': self.neo.name,
                    'diameter_km': self.neo.diameter,
                    'potentially_hazardous': self.neo.hazardous}
        }


# neo = NearEarthObject(**{'pdes': '433', 'name': 'Eros', 'diameter': 16.478903546, 'pha': 'N'})
# ca = CloseApproach(**{'des': "2015 ER", 'cd': "2000-Jan-01 01:48", 'dist': 0.144929491295557,'v_rel': 12.0338912415925, 'neo': neo})