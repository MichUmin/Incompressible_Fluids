import mesh_geometry_operations as geo
import boundaries

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
            match boundaries.type[f.boundary_name]:
                case 'do_nothing':
                    pass
                case 'Dirichlet':        
                    gamma_f = gamma.boundary_values[f.boundary_name]
                    d = geo.distance(p.centre, f.centre)
                    matrix[p_index][p_index] -= (-1.0)*gamma_f * geo.vec_len(f.area) / d
                    source[p_index][0] -= variable.boundary_values[f.boundary_name] * (-1.0)*gamma_f * geo.vec_len(f.area) / d
                case 'Neumann':
                    source[p_index][0] += geo.dot(f.area, variable.boundary_gradient[f.boundary_name])
                case _:
                    # catch all other boundary condition types
                    print('Invalid boundary condition')
                    quit()
        
                


def source(source_cell_index, variable, matrix, source_vector, mesh):
    # discretize source term in in Ax = b form
    # hard coded source term
    source_vector[source_cell_index][0] += 1.0

def convection(variable, velocity, matrix, source_vector, mesh):
    # convection_interpolation(variable, velocity, matrix, source_vector, mesh)
    convection_upstream(variable, velocity, matrix, source_vector, mesh)

def convection_interpolation(variable, velocity, matrix, source_vector, mesh):
    # discretize the convectionn operator in Ax = b form
    # linear interpolation of the variable value at the face
    num_faces = len(mesh.faces)
    for f_index in range(num_faces):
        # f = mesh.faces[f_index]
        p_index = mesh.faces[f_index].owner
        # p = mesh.cells[p_index]
        if mesh.faces[f_index].neighbour >= 0:
            # this is an internal face
            n_index = mesh.faces[f_index].neighbour
            # n = mesh.cells[n_index]
            f_x = mesh.faces[f_index].inter_coef
            u_f = [0.0, 0.0, 0.0]
            for i in range(3):
                u_f[i] = f_x*velocity.values[p_index][i] + (1.0 - f_x)*velocity.values[n_index][i]
            F = geo.dot(mesh.faces[f_index].area, u_f)
            matrix[p_index][p_index] += F*f_x
            matrix[n_index][n_index] -= F*(1.0-f_x)
            matrix[p_index][n_index] += F*(1.0-f_x)
            matrix[n_index][p_index] -= F*f_x
        else:
            # print(f_index, "neighbour:", mesh.faces[f_index].neighbour, "boundary_name:", mesh.faces[f_index].boundary_name)
            # this is a boundary face
            match boundaries.type[mesh.faces[f_index].boundary_name]:
                case 'do_nothing':
                    pass
                case 'Dirichlet':        
                    u_f = velocity.boundary_values[mesh.faces[f_index].boundary_name]
                    F = geo.dot(mesh.faces[f_index].area, u_f)
                    source_vector[p_index][0] -= F * variable.boundary_values[mesh.faces[f_index].boundary_name]
                case 'Neumann':
                    u_f = velocity.boundary_values[mesh.faces[f_index].boundary_name]
                    F = geo.dot(mesh.faces[f_index].area, u_f)
                    matrix[p_index][p_index] += F
                    vector_to_cell_centre = [0.0, 0.0, 0.0]
                    vector_to_cell_centre[0] = mesh.cells[p_index].centre.x - mesh.faces[f_index].centre.x
                    vector_to_cell_centre[1] = mesh.cells[p_index].centre.y - mesh.faces[f_index].centre.y
                    vector_to_cell_centre[2] = mesh.cells[p_index].centre.z - mesh.faces[f_index].centre.z
                    source_vector[p_index][0] += F*geo.dot(vector_to_cell_centre, variable.boundary_gradient[mesh.faces[f_index].boundary_name])
                case _:
                    # catch all other boundary condition types
                    print('Invalid boundary condition')
                    quit()

def convection_upstream(variable, velocity, matrix, source_vector, mesh):
    # discretize the convectionn operator in Ax = b form
    # linear interpolation of the variable value at the face
    num_faces = len(mesh.faces)
    for index in range(num_faces):
        f = mesh.faces[index]
        p_index = f.owner
        p = mesh.cells[p_index]
        if f.neighbour >= 0:
            # this is an internal face
            n_index = f.neighbour
            n = mesh.cells[n_index]
            PNvector = [0.0, 0.0, 0.0]
            PNvector[0] = n.centre.x - p.centre.x
            PNvector[1] = n.centre.y - p.centre.y
            PNvector[2] = n.centre.z - p.centre.z
            f_x = f.inter_coef
            u_f = [0.0, 0.0, 0.0]
            for i in range(3):
                u_f[i] = f_x*velocity.values[p_index][i] + (1.0 - f_x)*velocity.values[n_index][i]
            F = geo.dot(f.area, u_f)
            flow_direction = geo.dot(PNvector, u_f) # if flow_direction is positive the flow is from P to N
                                                    # if it is negative the flow is from N to P
            if (flow_direction >= 0.0):
                # flow from P to N
                matrix[p_index][p_index] += F
                matrix[n_index][n_index] -= 0.0
                matrix[p_index][n_index] += 0.0
                matrix[n_index][p_index] -= F
            else:
                # flow from N to P
                matrix[p_index][p_index] += 0.0
                matrix[n_index][n_index] -= F
                matrix[p_index][n_index] += F
                matrix[n_index][p_index] -= 0.0
        else:
            # this is a boundary face
            match boundaries.type[f.boundary_name]:
                case 'do_nothing':
                    pass
                case 'Dirichlet':        
                    u_f = velocity.boundary_values[f.boundary_name]
                    F = geo.dot(f.area, u_f)
                    source_vector[p_index][0] -= F * variable.boundary_values[f.boundary_name]
                case 'Neumann':
                    u_f = velocity.boundary_values[f.boundary_name]
                    F = geo.dot(f.area, u_f)
                    matrix[p_index][p_index] += F
                    vector_to_cell_centre = [0.0, 0.0, 0.0]
                    vector_to_cell_centre[0] = p.centre.x - f.centre.x
                    vector_to_cell_centre[1] = p.centre.y - f.centre.y
                    vector_to_cell_centre[2] = p.centre.z - f.centre.z
                    source_vector[p_index][0] += F*geo.dot(vector_to_cell_centre, variable.boundary_gradient[f.boundary_name])
                case _:
                    # catch all other boundary condition types
                    print('Invalid boundary condition')
                    quit()