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

# for i in OBJ_DICT:
#     print i,'\n', OBJ_DICT[i], '\n\n'

DIFFICULTY = OBJ_DICT["Difficulty"]
print DIFFICULTY

HIT_ITEMS = OBJ_DICT["HitObjects"]
#print HIT_ITEMS

def filter_items(start,end):
    #reaction time in millis
    AR = DIFFICULTY["ApproachRate"]
    time = 1200
    if AR < 5:
        time+=(5-AR)* 120
    else:
        time-=(AR-5)* 150
    v = 600/time
    in_interval = lambda item: item["t"] <= end+time and item["t"] >= start+time
    
