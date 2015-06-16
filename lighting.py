from gmath import *
from display import *

def get_light(p0, p1, p2):
    l = [p0, p1, p2]
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
            ]
    for rgb in light:
        if rgb > 255:
            rgb = 255
    return light
    
def ambient_light():
    return AMBIENT

def diffuse_light(center, p0, p1, p2):
    Id = [0,0,0]
    v1 = [p1[i]-p0[i] for i in range(len(p0))]
    v2 = [p0[i]-p2[i] for i in range(len(p0))]
    N = normalize(calculate_normal(v1[0], v1[1], v1[2], v2[0], v2[1], v2[2]))
    for li in LIGHTS:
        L = normalize([li[i]-center[i] for i in range(len(center))])
        dota2 = sum([L[i]*N[i] for i in range(len(N))])
        if dota2 > 0:
            for i in range(3,6):
                Id[i-3] += dota2*li[i]
    return [Id[i] * DIFFUSE[i] for i in range(len(Id))]
    
def specular_light(center, p0, p1, p2):
    Is = [0,0,0]
    v1 = [p1[i]-p0[i] for i in range(len(p0))]
    v2 = [p0[i]-p2[i] for i in range(len(p0))]
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
    return [Is[i] * SPECULAR[i] for i in range(len(Is))]
    
