import mesh_geometry_operations as geo

def time_derivative(variable, time_step, matrix, source, mesh):
    N = len(variable)
    for index in range(N):
        matrix[index][index] += (mesh.cells[index].volume) / time_step
        source[index][0] += variable[index][0] * (mesh.cells[index].volume) / time_step

def diffusion(variable, gamma, matrix, source, mesh):
    num_faces = len(mesh.faces)
    for index in range(num_faces):
        f = mesh.faces[index]
        p_index = f.owner
        p = mesh.cells[p_index]
        if f.neighbour >= 0:
            # this is an internal face
            n_index = f.neighbour
            #print(p_index, n_index)
            n = mesh.cells[n_index]
            gamma_f = f.inter_coef*gamma[p_index] + (1.0 - f.inter_coef)*gamma[n_index]
            d = geo.distance(p.centre, n.centre)
            a_n = gamma_f * geo.vec_len(f.area) / d
            matrix[p_index][p_index] -= a_n
            matrix[n_index][n_index] -= a_n
            matrix[p_index][n_index] += a_n
            matrix[n_index][p_index] += a_n
        else:
            #this is a boundary face
            match f.boundary_type:
                case "do_nothing":
                    pass
                case "Dirichlet":
                   gamma_f = gamma[p_index]
                   d = geo.distance(p.centre, f.centre)
                   matrix[p_index][p_index] -= gamma_f / d
                   source[p_index][0] += f.boundary_value * gamma_f / d
                case _:
                    print("Unrecognized boundary condition")
                    quit()


        