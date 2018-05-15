def Input():
    month
    input_other = []
    input_fri = []
    input_sat = []
    input_sun = []
    line_count = 0
    f = open("test.txt")
    for line in f:
        if line_count == 0:
            month = line
        elif line_count%7 == 5:   
            input_fri.append(line)
        elif line_count%7 == 6:   
            input_sat.append(line)
        elif line_count%7 == 0 and line_count != 0:   
            input_sun.append(line) 

    f.close    
    return input_other, input_fri, input_sat, input_sun
