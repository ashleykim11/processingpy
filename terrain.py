def setup():
    global cols, rows, terrain
    size(600, 600, P3D)
    w = 600
    h = 600
    cols = w/scl
    rows = h/scl
    terrain = [[0] * rows for i in range(cols)]
    for y in range (rows):
        for x in range (cols):
            terrain[x][y] = random(-10, 10)
    
def draw():
    global angle
    background(0)
    stroke(255)
    noFill()
    
    translate(width/2, height/2)
    rotateX(PI/3)
    translate(-width/2, -height/2)
    
    for y in range(rows-1):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols):
            vertex(x*scl,y*scl, terrain[x][y])
            vertex(x*scl,(y+1)*scl, terrain[x][y+1])
        endShape()
        
    noLoop()
            
