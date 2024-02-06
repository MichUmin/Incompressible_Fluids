import mesh_geometry_operations as geo

def time_derivative(variable, time_step, matrix, source, mesh):
    # dicretize time derivative in Ax = b form
    # first order dicretization
    N = len(mesh.cells)
    for index in range(N):
        matrix[index][index] += (mesh.cells[index].volume) / time_step
        source[index][0] += variable.values[index][0] * (mesh.cells[index].volume) / time_step

def diffusion(variable, gamma, matrix, source, mesh):
    # discretize the diffusion operator in Ax = b form
    # no non-orthogonality correction
    num_faces = len(mesh.faces)
    for index in range(num_faces):
        f = mesh.faces[index]
        p_index = f.owner
        p = mesh.cells[p_index]
        if f.neighbour >= 0:
            # this is an internal face
            n_index = f.neighbour
            n = mesh.cells[n_index]
            gamma_f = f.inter_coef*gamma.values[p_index] + (1.0 - f.inter_coef)*gamma.values[n_index]
            d = geo.distance(p.centre, n.centre)
            a_n = (-1.0)*gamma_f * geo.vec_len(f.area) / d
            matrix[p_index][p_index] -= a_n
            matrix[n_index][n_index] -= a_n
            matrix[p_index][n_index] += a_n
            matrix[n_index][p_index] += a_n
        else:
            # this is a boundary face
            if (f.boundary_type != 'do_nothing'):   # ugly bug fix         
                gamma_f = gamma.boundary_values[f.boundary_type]
                d = geo.distance(p.centre, f.centre)
                matrix[p_index][p_index] -= (-1.0)*gamma_f / d
                source[p_index][0] -= variable.boundary_values[f.boundary_type] * (-1.0)*gamma_f / d


def source(variable, matrix, source, mesh):
    # discretize source term in in Ax = b form
    # hard coded source term
    num_cells = len(mesh.cells)
    for i in range(num_cells):
        source[i][0] += 0.0