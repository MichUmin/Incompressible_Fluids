import math

def velocity(velocity_field, mesh):
    pass

def variable(variable_vector, mesh):
    N = len(variable_vector)
    for index in range(N):
        position = 0.01*index + 0.005
        variable_vector[index] = [math.sin(position*2.0*math.pi)]

def diffusion_coef(gamma_vector, mesh):
    N = len(gamma_vector)
    for index in range(N):
        gamma_vector[index] = [1.0]

def boundary_condition(mesh):
    mesh.faces[0].boundary_value = 0.0
    mesh.faces[100].boundary_value = 0.0
