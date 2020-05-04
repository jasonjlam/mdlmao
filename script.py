import mdl
from display import *
from matrix import *
from draw import *


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        line = command["op"]
        args = command["args"]
        if "constants" in command:
            if command['constants']!=None:
                reflect = command['constants']
            else:
                reflect = '.white'
        if line == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif line == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif line == 'box':
            #print 'BOX\t' + str(args)
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []

        elif line == 'line':
            #print 'LINE\t' + str(args)

            add_edge( tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif line == 'pop':
            stack.pop()

        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
        print(command)


def parse_stl_ascii( fname):

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    f = open(fname)
    lines = f.readlines()
    clear_screen(screen)
    clear_zbuffer(zbuffer)
    step = 100
    step_3d = 20

    symbols = {'.meme': ['constants',
                         {'red': [0.3, 0.77, 0.19],
                          'green': [0.3, 0.56, 0.14],
                          'blue': [0.3, 0.37, 0.09]}]}
    c = 0
    while c < len(lines):
        line = lines[c].strip()
        if line == "outer loop":
            c+=1
            arg0 = lines[c].strip().split(' ')
            c+=1
            arg1 = lines[c].strip().split(' ')
            c+=1
            arg2 = lines[c].strip().split(' ')
            add_polygon(tmp, float(arg0[1]), float(arg0[2]), float(arg0[3]),
                        float(arg1[1]), float(arg1[2]), float(arg1[3]), float(arg2[1]), float(arg2[2]), float(arg2[3]))
        c+=1

    t = make_translate(250, 60, 0)
    matrix_mult(stack[-1], t)
    stack[-1] = [x[:] for x in t]

    t = make_scale(6, 6, 6)
    matrix_mult(stack[-1], t)
    stack[-1] = [x[:] for x in t]

    t = make_rotY(-5.0 * (math.pi / 180))
    matrix_mult(stack[-1], t)
    stack[-1] = [x[:] for x in t]


    t = make_rotX(-80.0 * (math.pi / 180))
    matrix_mult(stack[-1], t)
    stack[-1] = [x[:] for x in t]

    matrix_mult(stack[-1], tmp)
    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, '.meme')
    display(screen)
