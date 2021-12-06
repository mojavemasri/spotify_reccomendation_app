#take all the data from the file as specified and turn it into a 2D array with each row a record
#then convert everything into the 4 table values then insert

#however what we really want is tuples but well get to that in a second
def array2d(filename):
    rs = []
    f = open(filename,"r")
    records = f.readlines()
    for i in range(len(records)):
        if i != 0:
            inst = records[i].split(',')
            inst.append(i)
            id = ord(inst[6][0])
            inst.append(id)
            rs.append(inst)
    return rs

#lst is list of indices that will be used for that particular tuple
#data is the array in question
def toTuples(lst, data):
    table = []
    for i in range(len(data)):
        temp = []
        for j in range(len(lst)):
            x = data[i]
            d = lst[j]
            temp.append(x[d])
        table.append(tuple(temp))
    table = clean(table)
    return table

#if a list has duplicate entries it will be removed here
def clean(data):
    cleaned = []
    for i in data:
        unique = True
        for j in cleaned:
            if i == j:
                unique = False
        if unique:
            cleaned.append(i)
    return cleaned
