#gas = { "width": 3, "height": 4, "state": [ [], ['l','w','r'], [],['r','l'], ['w'], [],[], [], [],[], [], [] ] }




def step(gas):

    # Particle collisions
    
    for cell in xrange(len(gas['state'])):
        # Following if statement handles reversing direction
        # of particles colliding with wall
        if 'w' in gas['state'][cell]:
            gas['state'][cell] = map(reverse,gas['state'][cell])
        elif len(gas['state'][cell]) == 2: #check if cell is not empty
            gas['state'][cell] = particle_collision(gas['state'][cell])

    
    
    # Particle propagation    
    next_state = [[] for i in xrange(len(gas['state']))]   

    for row in xrange(gas['height']):
        for col in xrange(gas['width']):
            index = col + (gas['width'] * row)
            if gas['state'][index]:
                for d in gas['state'][index]:         
                    if d != 'w':
                        new_index = move(d,row,col,gas['width'] )
                        next_state[new_index].append(d)
                    else:
                        next_state[index].append(d)
    

    #print sum([len(lst) for lst in next_state])
                    

    gas['state'] = next_state

    #print("AFTER PROPAGATION", gas)

    return gas
              

def move(direction,row,col,width):
    if direction == 'u':
        return col + (width * (row-1))
    elif direction == 'd':
        return col + (width * (row+1))
    elif direction == 'l':
        return (col-1) + (width * row)
    elif direction == 'r':
        return (col+1) + (width * row)
    else:
        return col + width * row
            
# handles two particles colliding
def particle_collision(cell):
    if 'l' in cell and 'r' in cell:
        return ['u','d']
    elif  'u' in cell and 'd' in cell:
        return ['l','r']
    return cell
            
def reverse(direction):
    if direction == 'u':
        return 'd'
    elif direction == 'd':
        return 'u'
    elif direction == 'l':
        return 'r'
    elif direction == 'r':
        return 'l'
    else:
        return 'w'
    
        
