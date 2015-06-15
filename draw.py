from display import *
from matrix import *
from gmath import calculate_dot
from math import cos, sin, pi
import sys
from random import randint

MAX_STEPS = 100

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )

#zbuffer
z_buffer = [[-sys.maxint for i in xrange(500)] for i in xrange(500)]
def reset_zbuf():
    for i in range(500):
        for j in range(500):
            z_buffer[j][i] = -sys.maxint

#scanline draws
#-- p0=bottom, p1=mid, p2=top
def scanline_convert(p, p1, p2, screen, color=[randint(0,255),randint(0,255),randint(0,255)]):
    for rgb in range(len(color)):
        color[rgb] = randint(0,255)

    #gotta draw dat triangle tho
    draw_line(screen, p[0], p[1], p[2], p1[0], p1[1], p1[2], color)
    draw_line(screen, p[0], p[1], p[2], p2[0], p2[1], p2[2], color)
    draw_line(screen, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], color)

    #god bless http://stackoverflow.com/questions/21068315/python-sort-first-element-of-list
    sorted_points = [p, p1, p2]
    sorted_points.sort(key = lambda x: x[1])
    b = sorted_points[0]
    m = sorted_points[1]
    t = sorted_points[2]
    '''
    dy1 = int(round(m[1] - b[1]) + 1)
    dy2 = int(round(t[1] - m[1]))
    
    for d1 in range(dy1):
            x1 = (m[0]*d1 + b[0]*(dy1-d1))/dy1
            z1 = (m[2]*d1 + b[2]*(dy1-d1))/dy1
            
            x2 = (t[0]*d1 + b[0]*(dy1+dy2-d1))/(dy1+dy2)
            z2 = (t[2]*d1 + b[2]*(dy1+dy2-d1))/(dy1+dy2)

            y = b[1] + d1
            draw_line(screen, x1, y, z1, x2, y, z2, color)
    
    for d2 in range(dy2):
            x1 = (m[0]*(dy2-d2) + t[0]*d2)/dy2
            z1 = (m[2]*(dy2-d2) + t[2]*d2)/dy2
            
            x2 = (b[0]*(dy2-d2) + t[0]*(dy1+d2))/(dy1+dy2)
            z2 = (b[2]*(dy2-d2) + t[2]*(dy1+d2))/(dy1+dy2)

            y = m[1] + d2
            draw_line(screen, x1, y, z1, x2, y, z2, color)
     '''
    
    x1 = b[0]
    x2 = b[0]
    dx1 = (t[0]-b[0])/int(t[1]-b[1])
    dx2 = (m[0]-b[0])/int(m[1]-b[1])
    
    y = b[1]
    
    z1 = b[2]
    z2 = b[2]
    dz1 = (t[2]-b[2])/int(t[1]-b[1])
    dz2 = (m[2]-b[2])/int(m[1]-b[1])
    
    while y < m[1]:
        x1 += dx1
        x2 += dx2
        y += 1
        z1 += dz1
        z2 += dz2
        draw_line(screen, int(x1), int(y), int(z1), int(x2), int(y), int(z2), color)

    x2 = m[0]
    dx2 = (t[0]-m[0])/int(t[1]-m[1])
    
    z2 = m[2]
    dz2 = (t[2]-m[2])/int(t[1]-m[1])
    
    while x2 < t[1]:
        x1 += dx1
        x2 += dx2
        y += 1
        z1 += dz1
        z2 += dz2
        draw_line(screen, int(x1), int(y), int(z1), int(x2), int(y), int(z2), color)
    
    
def draw_polygons( points, screen, color ):
    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return
    p = 0
    while p < len( points ) - 2:
        if calculate_dot( points, p ) >= 0:
            #-- calculate positions
            top=0;
            mid=0;
            bottom=0;
            min_value = min(points[p][1], min(points[p+1][1],points[p+2][1]));
            max_value = max(points[p][1], max(points[p+1][1],points[p+2][1]));
            if min_value == points[p][1] :
                bottom=0
            elif min_value == points[p+1][1]:
                bottom=1
            else:
                bottom=2
            if max_value == points[p][1]:
                top=0
            elif max_value == points[p+1][1]:
                top=1
            else:
                top=2
            mid = max(top,bottom) - min(top,bottom) + ( (max(top,bottom)-2)*-2 ) - 1
            #-- apply scanline
            top = points[p + top]
            mid = points[p + mid]
            bottom = points[p + bottom]
            scanline_convert(top,mid,bottom,screen)
            ##########scanline ends here
            draw_line( screen, points[p][0], points[p][1], points[p][2],
                       points[p+1][0], points[p+1][1], points[p+1][2], color)
            draw_line( screen, points[p+1][0], points[p+1][1], points[p+1][2],
                       points[p+2][0], points[p+2][1], points[p+2][2], color )
            draw_line( screen, points[p+2][0], points[p+2][1], points[p+2][2],
                       points[p][0], points[p][1], points[p][2], color )
            
        p+= 3
        
        


def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2], color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

#returns the z value on the line.
def calculate_z(start_value,end_value,current_value,start_z,end_z):
    if start_value-end_value ==0:
        return end_z
    percent=(current_value-start_value)/(end_value-start_value)
    return (end_z-start_z)*percent + start_z

def draw_line( screen, x0, y0, z0, x1, y1, z1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            z = calculate_z(y0,y1,y,z0,z1)
            if (y<len(z_buffer) and x0 <len(z_buffer) and z > z_buffer[int(y)][int(x0)]):
                plot(screen, color,   x0, y)
                z_buffer[int(y)][int(x0)] = z
                
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            z = calculate_z(x0,x1,x,z0,z1)
            if (y0<len(z_buffer) and x <len(z_buffer) and z_buffer[int(y0)][int(x)] <= z):
                plot(screen, color, x, y0)
                z_buffer[int(y0)][int(x)] = z
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            z = calculate_z(x0,x1,x,z0,z1)
            if (y0<len(z_buffer) and x <len(z_buffer) and z_buffer[int(y0)][int(x)] <= z):
                z_buffer[int(y0)][int(x)] = z
                plot(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            z = calculate_z(y0,y1,y,z0,z1)
            if (y<len(z_buffer) and x <len(z_buffer) and z_buffer[int(y)][int(x)] <= z):
                z_buffer[int(y)][int(x)] = z
                plot(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            #calc z, zbuf. x0 x1 x z0 z1
            z = calculate_z(x0,x1,x,z0,z1)
            if (y<len(z_buffer) and x <len(z_buffer) and z_buffer[int(y)][int(x)] <= z):
                z_buffer[int(y)][int(x)] = z
                plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            # " " y0 y1 y z0 z1
            z = calculate_z(y0,y1,y,z0,z1)
            if (y<len(z_buffer) and x <len(z_buffer) and z_buffer[int(y)][int(x)] <= z):
                z_buffer[int(y)][int(x)] = z
                plot(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

