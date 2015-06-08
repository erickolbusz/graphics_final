def parse(f_name):
    f = open(f_name, 'r')
    specs_dict = {}
    header_next = False
    for line in f.readlines():
        line = line.strip()
        if header_next and len(line) != 0:
            header = line[1:-1]
            print header
        header_next = (len(line) == 0)

parse("goreshit - o'er the flood (grumd) [The Flood Beneath].osu")
