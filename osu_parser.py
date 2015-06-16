global OBJ_DICT

def parse(f_name):
    f = open(f_name, 'r')
    specs_dict = {}
    combo_colors = []
    color_i = 0
    obj_types = ['SPINNER','CIRCLE','SLIDER']
    header_next = False
    filling_dict = (False, None)
    for line in f.readlines():
        line = line.strip()
        if line[:2] != "//": #comments
            if filling_dict[0]:
                if (len(line) == 0):
                    filling_dict = (False, None)
                else:
                    if header == 'HitObjects':
                        obj = line.split(',')
                        for spec_i in range(len(obj)):
                            try:
                                obj[spec_i] = int(obj[spec_i])
                            except ValueError:
                                pass
                        obj.pop(1) #no ycor
                        '''
                        1 = circle
                        2 = slider
                        5 = circle (starts new combo)
                        6 = slider (starts new combo)
                        12 = spinner
                        '''
                        #We can use combo_colors since Colours is before HitObjects in the file
                        obj_type = obj[2]
                        if obj_type in [5,6]:
                            color_i = (color_i + 1)%len(combo_colors)
                        obj_dict = {'x': obj[0]
                                   ,'t': obj[1]
                                   ,'type': obj_types[obj_type % 4]
                                   ,'color': combo_colors[color_i] 
                                   }
                        if obj_dict['type'] == 'SLIDER':
                            obj_dict['curve'] = obj[4]
                            obj_dict['reps'] = obj[5] #VERY IMPORTANT: DEFAULT IS 1 (i.e. REPS = SLIDER REVERSE ARROWS - 1)
                            obj_dict['length'] = obj[6]
                        elif obj_dict['type'] == 'SPINNER':
                            obj_dict['length'] = obj[4]
                        specs_dict[header][obj[1]] = obj_dict
                    else:
                        colon_i = line.find(':')
                        spec = line[:colon_i].strip()
                        value = line[colon_i+1:].strip()
                        if header == 'Colours':
                            combo_colors.append([int(val) for val in value.split(',')])
                        elif not (header == 'General' and spec in ['SampleSet'
                                                                 ,'StackLeniency'
                                                                 ,'Mode'
                                                                 ,'LetterboxInBreaks'
                                                                 ,'Countdown'
                                                                 ]
                                 ):
                            try:
                                value = int(value)
                            except ValueError:
                                pass
                            specs_dict[header][spec] = value
            if header_next and len(line) != 0:
                header = line[1:-1]
                if header not in ['Editor', 'Metadata', 'Events', 'TimingPoints']:
                    specs_dict[header] = {}
                    filling_dict = (True, header)
            header_next = (len(line) == 0)
    specs_dict['Colours'] = combo_colors
    return specs_dict

global OBJ_DICT

OBJ_DICT = parse("goreshit - o'er the flood (grumd) [The Flood Beneath].osu")

DIFFICULTY = OBJ_DICT["Difficulty"]

HIT_ITEMS = OBJ_DICT["HitObjects"]

AR = DIFFICULTY["ApproachRate"]
time = 1200.0 # reaction time
if AR < 5:
    time+=(5-AR)* 120
else:
    time-=(AR-5)* 150
v = 500/time # velocity of items
#pixel per milliseconds

def filter_items(start,end):
    swag=[]
    for key in HIT_ITEMS.keys():
        x = HIT_ITEMS[key]
        if x["t"] >=  start and x["t"] < end+time:
            swag.append(x)
    newlist = sorted(swag,key = lambda k: k["t"])
    return newlist


def create_script(hit_objects,start_time,end_time):
    ##we make it 30 fps.
    ##t = milliseconds.
    ## t/33.333 = number of frames.
    
    f= open("ctf.mdl","w")
    f.write("frames 30\n")
    f.write("basename ctf\n")
    f.write("push\n")
    f.write("move 0 -" + str( (end_time-start_time)*v ) + " 0 drop\n")
    for each in hit_objects:
        f.write("sphere "+str(each["x"]/640.0*800) + " " + str(v*(each["t"]-start_time)) + " 0 30\n")
        if each["type"]=="SLIDER":
            reps = each["reps"]
            last_x = int(each["curve"].split("|")[-1].split(":")[0])
            interval = (abs(float(each["length"]) )/640.0*800)/v
            #print interval
            i=1
            while (reps > 0):
                if i%2==1:
                    f.write("sphere "+ str(last_x/640.0*800) + " " + 
                            str(v*(each["t"]-start_time + interval*i)) + " 0 30\n")
                else:
                    f.write("sphere "+ str(each["x"]/640.0*800) + " " + 
                            str(v*(each["t"]-start_time + interval*i)) + " 0 30\n")
                i+=1
                reps-=1
        ##for bezier
        #pass B|x:y|x:y through here, or at least the last x and the # of repeats.
        #add another hit sphere here too.
        ##
        
    f.write("pop\n")
    f.write("push\n")
    
    
    f.write("move " + str(400-hit_objects[0]["x"]) + " 0 0 KNOB1\n")
    f.write("move 0 200 0 KNOB2\n")
    

    f.write("box 400 100 0 50 60 10\n")
    
    #f.write("vary KNOB1 0 " +  (hit_objects[0]["t"] - start_ +  " 0 1\n")
    f.write("vary KNOB2 15 29 0 1\n")
    


    f.write("vary drop 0 29 0 1\n")
    f.close()
    
#nothing
first_list = filter_items(0,10000)

second_list = filter_items(15000,20000)
create_script(second_list,15000,20000)
