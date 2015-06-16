from matrix import *
from gmath import *
from display import *

def get_light(p0, p1, p2):
    I = [0,0,0]
    v1 = [p1[i]-p0[i] for i in range(len(p0))]
    v2 = [p2[i]-p0[i] for i in range(len(p0))]
    N = [ v1[1]*v2[2]-v1[2]*v2[1]
        , v1[2]*v2[0]-v1[0]*v2[2]
        , v1[0]*v2[1]-v1[1]*v2[0]]
    normalize(N)
    
    #ambient
    for i in range(len(AMBIENT)):
        I[i] = AMBIENT[i]

    for li in LIGHTS:
        #print I
        li_color = li[0]
        li_v = li[1]
        normalize(li_v)
        dota2 = sum([li_v[i]*N[i] for i in range(len(N))])
        
        #diffuse
        if dota2 > 0:
            for i in range(len(li_color)):
                I[i] += dota2*li_color[i]
        #print I
        #specular
        p = [ v1[1]*v2[2]-v1[2]*v2[1]
            , v1[2]*v2[0]-v1[0]*v2[2]
            , v1[0]*v2[1]-v1[1]*v2[0]]
        scalar_mult([p],dota2*2) #dota4??
        for i in range(len(p)):
            p[i] -= li[1][i] #haven't normalized yet, can't use v
        normalize(p)
        v =[0,0,-1]
        normalize(v)
        dota3 = sum([p[i]*v[i] for i in range(len(v))])
        if dota3 > 0:
            #congrats valvo
            dota3 = dota3 ** SPEC_K
            I[i] += dota3*li_color[i]
        #print I
            
        
        
    '''l = [p0, p1, p2]
    center = [ sum([p[0] for p in l])/3.0
             , sum([p[1] for p in l])/3.0
             , sum([p[2] for p in l])/3.0
             ]
    l_I = [ ambient_light()
          , diffuse_light(center, p0, p1, p2)
          , specular_light(center, p0, p1, p2)
          ]
    light = [ int(round(sum(I[0] for I in l_I)))
            , int(round(sum(I[1] for I in l_I)))
            , int(round(sum(I[2] for I in l_I)))
            ]'''
    
    for rgb in I:
        if rgb > 255:
            rgb = 255
    return I
    
'''
def ambient_light():
    return AMBIENT

def diffuse_light(center, p0, p1, p2):
    
    
def specular_light(center, p0, p1, p2):
    
    Is = [0,0,0]
    v1 = [p1[i]-p0[i] for i in range(len(p0))]
    v2 = [p2[i]-p0[i] for i in range(len(p0))]
    N = normalize(calculate_normal(v1[0], v1[1], v1[2], v2[0], v2[1], v2[2]))
    for li in LIGHTS:
        L = normalize([li[i]-center[i] for i in range(len(center))])
        dota2 = sum([L[i]*N[i] for i in range(len(N))])
        if dota2 > 0:
            R = [2*N[i]-L[i] for i in range(len(N))]
            dota3 = sum([L[i]*[0,0,-1][i] for i in range(len(L))]) #aka L[2]*-1 lol
            if dota3 > 0:
                #congrats valvo
                dota3 = dota3**SPEC_K
                for i in range(3,6):
                    Is[i-3] += dota3*li[i]
    return [Is[i] * SPECULAR[i] for i in range(len(Is))]'''
    
