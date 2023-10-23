#include <iostream>
#include <vector>
#include <cmath>

using std::vector;

class point
{
    private:
        const double __x;
        const double __y;
        const double __z;
    public:
        point(double co1, double co2, double co3): __x(co1), __y(co2), __z(co3) {}
        double x() const;
        double y() const;
        double z() const;
        vector<double> coordinates() const;
};
/*
class face
{
    private:
        const vector<point*> __vertices;
        point __centre;
        vector<double> __area;
    public:
        face(vector<point*>);
        vector<point*> vertices() const;
        vector<double> area() const;
        point centre() const;
        //cell* neighbour() const;
        //cell* owner() const;
};


class cell
{
    private:
        vector<face*> __faces;
        point __centre;
        double __volume;
    public:
        cell(vector<face*>);
        double volume() const;
        vector<cell*> neighbours() const;
};

class mesh
{
    private:
        vector<cell*> __cells;
        int __number_of_cells;
        int __number_of_faces;
        int __number_of_points;
    public:
        mesh(vector<cell*>, int, int, int);
        int n_points() const;
        int n_faces() const;
        int n_cells() const;
}
*/
/*
point::point(double x, double y, double z): __x(x), __y(y), __z(z)
{
    
    __x = x;
    __y = y;
    __z = z;
    
}
*/

double point::x() const
{
    return __x;
}

double point::y() const
{
    return __y;
}

double point::z() const
{
    return __z;
}

vector<double> point::coordinates() const
{
    vector<double> help;
    help.resize(3);
    help[0] = __x;
    help[1] = __y;
    help[2] = __z;
    return help;
}

void print(vector<double> to_print)
{
    int number = to_print.size();
    for (int index = 0; index < number; index++)
    {
        std::cout << to_print[index] << " ";
    }
    std::cout << std::endl;
}

vector<double> vec_area(point A, point B, point C)
{
    double AB_x = B.x() - A.x();
    double AB_y = B.y() - A.y();
    double AB_z = B.z() - A.z();
    double AC_x = C.x() - A.x();
    double AC_y = C.y() - A.y();
    double AC_z = C.z() - A.z();
    double cross_x = (AB_y * AC_z) - (AB_z * AC_y);
    double cross_y = (AB_z * AC_x) - (AB_x * AC_z);
    double cross_z = (AB_x * AC_y) - (AB_y * AC_x);
    vector<double> result;
    result.resize(3);
    result[0] = 0.5 * cross_x;
    result[1] = 0.5 * cross_y;
    result[2] = 0.5 * cross_z;
    return result;
}

double abs_area(point A, point B, point C)
{
    vector<double>  v_area = vec_area(A, B, C);
    double ans_2 = (v_area[0]*v_area[0]) + (v_area[1]*v_area[1]) + (v_area[2]*v_area[2]);
    return sqrt(ans_2);
}

/*
face::face(vector<*point> list): __vertices(list)
{
    //__vertices = list_of_vertices;
    int n_vertices = __vertices.size();
    double av_x = 0, av_y  = 0, av_z = 0;
    for (int i = 0; i < n_vertices; i++)
    {
        av_x += (*(__vertices[i])).x();
        av_y += (*__vertices[i]).y();
        av_z += (*__vertices[i]).z();
    }
    av_x = av_x / n_vertices;
    av_y = av_y / n_vertices;
    av_z = av_z / n_vertices;
    point temp_centre(av_x, av_y, av_z);
    double c_x = 0, c_y = 0, c_z = 0, temp_area = 0, tri_area;
    int next;
    for (int point = 0; point < n_vertices; point ++)
    {
        next = (point + 1) % n_vertices;
        tri_area = abs_area(temp_centre, *__vertices[point], *__vertices[next]);
        c_x += ((av_x + (*__vertices[point]).x() + (*__vertices[next]).x())*tri_area);
        c_y += ((av_y + (*__vertices[point]).y() + (*__vertices[next]).y())*tri_area);
        c_z += ((av_z + (*__vertices[point]).z() + (*__vertices[next]).z())*tri_area);
        temp_area += tri_area;
    }
    c_x = c_x / temp_area;
    c_y = c_y / temp_area;
    c_z = c_z / temp_area;
    point __centre(c_x, c_y, c_z);
    __area.resize(3);
    __area[0] = 0, __area[1] = 0, __area[2] = 0;
    vector<double> help_area;
    for (int point = 0; point < n_vertices; point ++)
    {
        next = (point + 1) % n_vertices;
        help_area = vec_area(__centre, *__vertices[point], *__vertices[next]);
        __area[0] += help_area[0];
        __area[1] += help_area[1];
        __area[2] += help_area[2];
    }
}

point face::centre() const
{
    return __centre;
}

vector<double> face::area() const
{
    return __area;
}

vector<point*> face::vertices() const
{
    return __vertices;
}


*/

int main()
{
    point p0(0, 0, 0);
    point p1(1, 0, 0);
    point p2(1, 1, 0);
    point p3(0, 1, 0);
    vector<point*> v = {&p0, &p1, &p2, &p3};
    //face c0(v);
    //print(c0.area());
    return 0;
}