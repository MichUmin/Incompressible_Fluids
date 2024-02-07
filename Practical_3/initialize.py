import math

def velocity(velocity_field, mesh):
    N = len(mesh.cells)
    for index in range(N):
        velocity_field.values[index] = [0.0, 0.0, 0.0]
    velocity_field.boundary_values = {'left': [0.0, 0.0, 0.0], 'right': [0.0, 0.0, 0.0], 'top': [0.0, 0.0, 0.0], 'bottom': [0.0, 0.0, 0.0], 'do_nothing': [0.0, 0.0, 0.0]}

# def variable(variable_vector, mesh):
#     N = len(variable_vector)
#     for index in range(N):
#         position = 0.01*index + 0.005
#         variable_vector[index] = [math.sin(position*2.0*math.pi)]

def variable(variable_vector, mesh):
    N = len(mesh.cells)
    for index in range(N):
        variable_vector.values[index] = [1.0]
    variable_vector.boundary_values = {'left': -1.0, 'right': 2.0, 'top': 1.0, 'bottom': -1.0, 'do_nothing': 0.0}


def diffusion_coef(gamma_vector, mesh):
    N = len(mesh.cells)
    for index in range(N):
        gamma_vector.values[index] = [1.0]
    gamma_vector.boundary_values =  {'left': 1.0, 'right': 1.0, 'top': 1.0, 'bottom': 1.0, 'do_nothing': 0.0}

# def boundary_condition(mesh):
#     mesh.faces[0].boundary_value = 1.0
#     mesh.faces[100].boundary_value = 4.0


