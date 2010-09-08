#!/usr/bin/env python

cdef extern from "math.h":
    double sqrt(double)

cimport numpy as np
import numpy as np



def calc_wire_B_field(np.ndarray[np.double_t, ndim=2] wire_nodes not None, 
                        np.ndarray[np.double_t, ndim=2] points not None,
                        double radius):
    cdef:
        np.ndarray[np.double_t, ndim=2] output
        int n_nodes = wire_nodes.shape[0]
        int n_points = points.shape[0]
        int i,j
        double rx, ry, rz, r, lx, ly, lz, #l
        double ax, ay, az
        double bx, b_y, bz
        double ox, oy, oz
        
    assert wire_nodes.shape[1]==3
    assert points.shape[1]==3
    output = np.empty_like(points)
    for i in xrange(n_points):
        bx = wire_nodes[n_nodes-1,0]
        b_y = wire_nodes[n_nodes-1,1]
        bz = wire_nodes[n_nodes-1,2]
        ox = oy = oz = 0.0
        for j in xrange(n_nodes):
            ax = wire_nodes[j,0]
            ay = wire_nodes[j,1]
            az = wire_nodes[j,2]
            lx = ax-bx
            ly = ay-b_y
            lz = az-bz
            #l = sqrt(lx*lx + ly*ly + lz*lz)
            #if l > radius:
            #else:
            rx = points[i,0] - ((ax+bx)/2.)
            ry = points[i,1] - ((ay+b_y)/2.)
            rz = points[i,2] - ((az+bz)/2.)
            r = sqrt(rx*rx + ry*ry + rz*rz)
            if r < radius:
                r = radius*radius*radius
            else:
                r = r*r*r
            ox += ((ry*lz) - (rz*ly))/r
            oy += ((rz*lx) - (rx*lz))/r
            oz += ((rx*lz) - (ry*lx))/r
            bx = ax
            b_y = ay
            bz = az
        output[i,0] = ox
        output[i,1] = oy
        output[i,2] = oz
    return output