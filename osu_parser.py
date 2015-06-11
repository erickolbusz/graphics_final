def parse(f_name):
    f = open(f_name, 'r')
    specs_dict = {}
    header_next = False
    filling_dict = (False, None)
    for line in f.readlines():
        line = line.strip()
        if filling_dict[0]:
            if (len(line) == 0):
                filling_dict = (False, None)
            else:
                if header != 'HitObjects':
                    colon_i = line.find(':')
                    spec = line[:colon_i]
                    value = line[colon_i+1:]
                    try:
                            value = int(value)
                    except ValueError:
                        pass
                    specs_dict[header].append((spec, value))
                specs_dict[header].append(line)
        if header_next and len(line) != 0:
            header = line[1:-1]
            if header not in ['Editor', 'Events']:
                specs_dict[header] = []
                filling_dict = (True, header)
        header_next = (len(line) == 0)
    return specs_dict

d = parse("goreshit - o'er the flood (grumd) [The Flood Beneath].osu")
