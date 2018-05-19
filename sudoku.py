#
# Sudoku solver
#   Simple version
#

import sys

# 5: hard
EXAMPLE_ID = 5

def setup_grid(id):
    # Easy
    if id == 1:
        grid  = "000000000"
        grid += "000000027"
        grid += "400608000"
        grid += "071000300"
        grid += "238506419"
        grid += "964100750"
        grid += "395027800"
        grid += "182060974"
        grid += "046819205"
    # Easy
    elif id == 2:
        grid  = "003020600"
        grid += "900305001"
        grid += "001806400"
        grid += "008102900"
        grid += "700000008"
        grid += "006708200"
        grid += "002609500"
        grid += "800203009"
        grid += "005010300"

    # Easy
    elif id == 3:
        grid  = "000000000"
        grid += "000000140"
        grid += "500076080"
        grid += "012400000"
        grid += "000000000"
        grid += "000305006"
        grid += "000100000"
        grid += "600000007"
        grid += "003009000"
    # Middel
    elif id == 4:
        grid  = "000000000"
        grid += "000000280"
        grid += "376400000"
        grid += "700001000"
        grid += "020000000"
        grid += "400300006"
        grid += "010028000"
        grid += "000005000"
        grid += "000000003"

    #
    elif id == 5:
        grid  = "000009700"
        grid += "004000000"
        grid += "002000008"
        grid += "000260003"
        grid += "091000000"
        grid += "070000000"
        grid += "000800002"
        grid += "010000900"
        grid += "008300000"

    # Very hard
    elif id == 6:
        grid = ".....6....59.....82....8....45........3........6..3.54...325..6.................."
        grid = grid.replace(".", "0")
    return grid


full_list = 0b111111111

def gen_list(b):
    l = []
    for i in range(9):
        mask = 1 << i
        if (mask & b) != 0:
            l.append(mask)
    return l

def count_bit(b):
    c = 0
    for i in range(9):
        if (b & (1<<i)) != 0:
            c += 1
    return c

def gen_bit_array(grid):
    ret = []
    for c in grid:
        i = int(c)
        ret.append(0 if i == 0 else 1 << (i-1))
    return ret

def candidate(grid, ppoint, debug=False):
    (x, y) = ppoint
    now = grid[x+y*9]
    if debug:
        print("now=%s"%now)
    candidate = full_list

    # Line
    l = grid[y*9: y*9+9]
    # Column
    l.extend(grid[x:81:9])
    # Block
    x0 = int(x/3)*3
    y0 = int(y/3)*3
    r = y % 3
    if r != 0:
        l.extend(grid[x0+y0*9:x0+3+y0*9])
    y0 += 1
    if r != 1:
        l.extend(grid[x0+y0*9:x0+3+y0*9])
    y0 += 1
    if r != 2:
        l.extend(grid[x0+y0*9:x0+3+y0*9])
    m = 0

    for lc in l:
        m |= lc
    candidate &= ~m
    return candidate

def find_bit(b):
    for i in range(0,9):
        mask = 1 << i
        if (mask & b)  != 0:
            return str(i+1)
    return "0"

def display_grid(grid, debug=False):
    #print(find_bit(grid[15]))
    #print(grid[23])
    for i in range(0,81,9):
        if debug:
            print(i)
        #l = grid[i:i+9]
        #print(l[:3], l[3:6], l[6:9])
        bstr = ""
        for j in range(0, 9):
            if debug:
                print("i+j=%d, => %s" % (i+j, bin(grid[i+j])))
                print(" find_bit, res:%s" % find_bit(grid[i+j]))
            bstr += find_bit(grid[i+j])
        print("%s %s %s" % (bstr[:3], bstr[3:6], bstr[6:9]))

        ln = i/9
        if (ln%3) == 2:
            print

def is_full(grid):
    for i in range(0,81,9):
        b = 0
        for j in range(0, 9):
            b |= grid[i+j]
        if b == 0b111111111:
            continue
        else:
            return False
    return True

def solver(grid, debug=False):
    if is_full(grid):
        return True, grid

    # 0: nothing, 9:full
    alen = [[] for i in range(10)]
    for iy in range(9):
        for ix in range(9):
            if grid[iy*9+ix] != 0:
                continue
            clist = candidate(grid, (ix, iy), debug)
            if debug:
                print("@(%d,%d) clist :%s" % (ix, iy, bin(clist)))
            alen[count_bit(clist)].append(([ix, iy], clist))

    for i in range(10):
        if len(alen[i]) != 0:
            if debug:
                print("Count=%d:" % i)
            for point in alen[i]:
                if debug:
                    print(" Point:", point)
                xy, clist = point
                [ix, iy] = xy
                cclist = gen_list(clist)
                #print(" Cclist:", cclist)
                for cc in cclist:
                    # Save
                    #print("Index:%d" % (ix+iy*9))
                    oc = grid[ix+iy*9]
                    #print(" oc=%s" % oc)
                    grid[ix+iy*9] = cc
                    #print(" new val=%s" % bin(cc))
                    if debug:
                        print("New grid@(%d,%d)=>%s:"% (ix,iy, cc))
                        #print(grid)
                        display_grid(grid)
                    ok, grid = solver(grid, debug)
                    if ok:
                        return ok, grid
                    # Restore
                    grid[ix+iy*9] = oc
                if debug:
                    print("False at (%d,%d), clist=%s" % (ix, iy, clist))
                return False, grid

    return False, grid


if __name__ == "__main__":

    args = sys.argv
    argc = len(args)
    if False:
        print(args)
        print(argc)
    if argc != 2:
        print("Usage: python sudoku.py ID(1-6)")
        sys.exit(-1)
    id = int(args[1])

    print(" ID: [%d]" % id)
    grid = setup_grid(id)
    print(" Input:")
    bgrid = gen_bit_array(grid)
    #print(bgrid)
    display_grid(bgrid, False)

    #print(is_full(bgrid))
    status, rgrid = solver(bgrid, False)
    print(" =>Result:")
    if status:
        display_grid(rgrid)
