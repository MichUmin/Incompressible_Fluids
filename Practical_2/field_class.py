import numpy

class scalar_field:
    def __init__(self, size):
        self.values = numpy.zeros((size,1))
        self.boundary_values = {}


class vector_field:
    def __init__(self, size):
        self.values = numpy.zeros((size,3))
        self.boundary_values = {}