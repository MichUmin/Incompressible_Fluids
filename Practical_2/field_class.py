import numpy

class field:
    def __init__(self, size):
        self.values = numpy.zeros((size,1))
        self.boundary_values = {}