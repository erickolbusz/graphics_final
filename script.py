import mdl
from display import *
from matrix import *
from draw import *
import copy

basename = "image"
frames = 1

"""======== first_pass(commands, symbols ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  jdyrlandweaver
  ==================== """

def first_pass(commands):
    found_frames = 0
    frames_first = False
    is_anim = False
    if commands[0][0] == "frames":
        frames_first = True
    for command in commands:
        cmd = command[0]
        if cmd == "frames":
            found_frames += 1
    if not frames_first and found_frames > 0:
        print "Please define the number of frames in the first line of the script."
        exit(2)
    if found_frames > 1:
        print "Please only define the number of frames once per script."
        exit(2)
    if frames_first and found_frames == 1:
        frame_count = commands[0][1]
    else:
        frame_count = 1
    if frame_count < 1:
        print "Must have at least 1 frame in image."
        exit(2)
    if frame_count > 1:
        is_anim = True

    has_vary = False
    for command in commands:
        cmd = command[0]
        if cmd == "vary":
            has_vary = True
            break

    has_basename = False
    use_default = False
    found_basename = 0
    for command in commands:
        cmd = command[0]
        if cmd == "basename":
            found_basename += 1
    if found_basename > 1:
        print "Please only define the basename once per script."
        exit(2)
    if found_basename == 1:
        if commands[1][0] == "basename":
            has_bas5ename = True
    if found_basename == 0:
        use_default = True
        print 'No basename defined, using "image" as file prefix.'
    
    if has_vary and not is_anim:
        print "No animation found with vary command."
        exit(2)
    if is_anim:
        global frames
        frames = commands[0][1]
    if has_basename:
        global basename
        basename = commands[1][1]
        
"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""        

def second_pass(commands):
    global frames
    knobs = []
    for frame in range(frames):
        #because apparently having knobs [{}]*frames breaks everything in your code even though it should make no difference :)
        knobs.append({})
    for cmd in commands:
        if cmd[0] == "vary":
            knob_name = cmd[1]
            start_frame = cmd[2]
            end_frame = cmd[3]
            if not (0 <= start_frame < frames) or not (0 <= end_frame < frames):
                print "Knob %s out of bounds."%(knob_name)
                exit(2)
            start_value = cmd[4]
            end_value = cmd[5]
            change_per_frame=0
            if (end_frame != start_frame):
                change_per_frame = float(end_value-start_value)/float(end_frame-start_frame)
            
            for frame in range(frames):
                if frame < start_frame:
                    knobs[frame][knob_name] = start_value
                elif frame > end_frame:
                    knobs[frame][knob_name] = end_value
                else:
                    knobs[frame][knob_name] = start_value + change_per_frame*(frame-start_frame)
    return knobs
    
def run(filename):    
    tmp = new_matrix()
    ident(tmp)
    stack = [tmp]
    screen = new_screen()

    
    def mult(m):
        matrix_mult(stack[len(stack)-1], m)
        stack[len(stack)-1] = m    

    p = mdl.parseFile(filename)
    
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    
    first_pass(commands)
    knobs = second_pass(commands)

    global basename
    global frames
    
    for frame in range(frames):
        color = [255, 255, 255]
        #print color
        #frames = 1 means no animation aka static image
        for command in commands:
            if not stack:
                stack = [tmp]
            cmd = command[0]
            k = 1
            if cmd == "push":
                stack.append(copy.deepcopy(stack[len(stack)-1]))
            if cmd == "pop":
                stack.pop()
            if cmd == "color":
                color = [command[1], command[2], command[3]]
            if cmd == "move":
                if frames > 1 and command[4] in knobs[frame]:
                    k = knobs[frame][command[4]]
                mult(make_translate(command[1]*k, command[2]*k, command[3]*k))
            if cmd == "rotate":
                if frames > 1 and command[3] in knobs[frame]:
                    k = knobs[frame][command[3]]
                t = k*command[2]*math.pi/180
                #print t
                axis = command[1]
                if axis == 'x':
                    mult(make_rotX(t))
                if axis == 'y':
                    mult(make_rotY(t))
                if axis == 'z':
                    mult(make_rotZ(t))
            if cmd == "scale":
                if frames > 1 and command[4] in knobs[frame]:
                    k = knobs[frame][command[4]]
                mult(make_scale(command[1]*k, command[2]*k, command[3]*k))
            if cmd in ["box", "sphere", "torus"]:
                polygons = []
                if cmd == "box":
                    add_box(polygons, command[1],command[2],command[3],command[4],command[5],command[6])
                if cmd == "sphere":
                    add_sphere(polygons, command[1],command[2],command[3],command[4],5)
                if cmd == "torus":
                    add_torus(polygons, command[1],command[2],command[3],command[4],command[5],5)
                matrix_mult(stack[len(stack)-1], polygons)
                draw_polygons(polygons, screen, color)
            if cmd == "line":
                points = []
                add_edge(points, command[1],command[2],command[3],command[4],command[5],command[6])
                matrix_mult(stack[len(stack)-1], points)
                draw_lines(polygons, screen, color)
            if cmd == "save":
                save_ppm(screen, cmd[1])
            if cmd == "display":
                display(screen)
        if frames > 1:
            save_extension(screen, "animations/" + basename + "%05d"%frame + ".png")
            screen = new_screen()
            stack = []
            reset_zbuf()

run("ctf.mdl")
#run("sphere.mdl")
