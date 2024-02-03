def velocity(velocity_field, mesh):
    pass

def variable(variable_vector, mesh):
    N = len(variable_vector)
    for index in range(N):
        if index % 2 == 0:
            variable_vector[index] = [1.0]
        else:
            variable_vector[index] = [1.0]

def diffusion_coef(gamma_vector, mesh):
    N = len(gamma_vector)
    for index in range(N):
        gamma_vector[index] = [1.0]
