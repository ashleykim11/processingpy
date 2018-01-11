# constant values
dirUp = 0    # 0
dirRight = 1 # 90
dirDown = 2  # 180
dirLeft = 3  # 270 degrees

mForward = 0
mBackward = 1
tRight = 1
tLeft = 3

# configuration values
resolution = 20
nRows = 0
nCols = 0
initialized = False
debug = False
spriteDir = dirRight
targetDir = dirRight
targetDirAngle = 0

spriteLoc = PVector(0, 0)  # in grids
spriteXY = PVector(0, 0)   # in pixel
targetLoc = PVector(0, 0)  
targetXY = PVector(0, 0) 
destination = PVector(0, 0) 
destinationXY = PVector(0, 0) 

speed = 1
turnSpeed = 1
roads = []
commands = []
orgCommands = []
curCommand = None
spriteSet = False
targetSet = False
destinationSet = False
animStart = False

def start():
    global animStart
    animStart = True

def test():
    print (commands)
    print (orgCommands)
    
def restart():
    global commands, orgCommands
    commands = list(orgCommands) # https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
    animStart = True
    print(commands)
    
    
def initGrid(r=20):
    global nRows, nCols, resolution, initialized
    nRows = height/r
    nCols = width/r
    initialized = True
    resolution = r
    
def showGrid(r=20, lineColor=155, lineWeight=1, index=False):
    """Display grid lines"""
    if (initialized == False):
        initGrid(r)
        
    pushStyle()
    stroke(lineColor)
    strokeWeight(1)
    for i in range(nRows):
        line(0, r*i, width, r*i)
    for i in range(nCols):
        line(r*i, 0, r*i, height)
        
    if (index):
        fill(255, 0, 0)
        for i in range(nRows):
            text(str(i), 0, r*(i+1))
        fill(0)
        for i in range(nCols):
            text(str(i), r*(i), 10)
    else:
        fill(0)
        text("   0", 0, 10)
        text(str(width), width - 20, 10)
        fill(255, 0, 0)
        text("0", 0, 10)
        text(str(height), 0, height)
        
    popStyle()
    
def addRoad(xg1, yg1, xg2, yg2):
    global roads
    roads.append((PVector(xg1, yg1), PVector(xg2, yg2)))
    
def printRoads():
    for i in range(len(roads)):
        print("road " + str(i+1) + ": " + str(roads[i][0].x) + " " + str(roads[i][0].y) + 
              " " + str(roads[i][1].x) + " " + str(roads[i][1].y)) 

        
def drawRoads():
    pushStyle()
    strokeWeight(20)
    stroke(255, 255, 0)
    #strokeCap(SQUARE)
    for i in range(len(roads)):
        rStart = gridToXY(roads[i][0])
        rEnd = gridToXY(roads[i][1])
        line(rStart.x, rStart.y, rEnd.x, rEnd.y)  
    popStyle()
 
def gridToXY(g):
    return (PVector(g.x*resolution + resolution/2, g.y*resolution + resolution/2))

def xyToGrid(loc):
    return (PVector(floor(loc.x / resolution), floor(loc.y / resolution)))
   
def setSprite(xg, yg, direction=1):
    global spriteLoc, spriteXY, spriteDir, spriteSet
    spriteLoc = PVector(xg, yg)
    spriteXY = gridToXY(spriteLoc)
    spriteDir = direction
    spriteSet = True

def printSprite():
    print("spriteLoc:" + str(spriteLoc.x) + " " + str(spriteLoc.y) + 
          "spriteXY:" + str(spriteXY.x) + " " + str(spriteXY.y))

def printTarget():
    print("targetLoc:" + str(targetLoc.x) + " " + str(targetLoc.y) + 
          " targetXY:" + str(targetXY.x) + " " + str(targetXY.y))

        
def setDestination(xg, yg):
    global destination, destinationXY, destinationSet
    destination = PVector(xg, yg)
    destinationXY = gridToXY(destination)
    destinationSet = True

def printDestination():
    print("destination:" + str(destination.x) + " " + str(destination.y))
    
    
def setTarget(xg, yg):
    global targetLoc, targetXY, targetSet
    targetLoc = PVector(xg, yg)
    targetXY = gridToXY(targetLoc)
    targetSet = True

def updateSprite():
    """ return true if reaching the target else return false"""
    global spriteLoc, sprintXY, targetSet,  commands 
    if (spriteXY == targetXY):  # reach the target
        print("reached target!")
        commands.pop(0)
        targetSet = False
        return True
    else:
        if (spriteDir == dirRight):
            spriteXY.x += speed
        elif (spriteDir == dirBottom):
            spriteXY.y += speed
        elif (spriteDir == dirLeft):
            spriteXY.x -= speed
        else:
            spriteXY.y -= speed
            
        spriteLoc = xyToGrid(spriteXY)

def drawSprite():
    # Draw a triangle rotated in the direction of velocity
    if (spriteSet == False):
        print("Sprite is not set")
        return
    
    dir = spriteDir
    if (dir == dirRight):
        theta = radians(90)
    elif (dir == dirDown):
        theta = radians(180)
    elif (dir == dirLeft):
        theta = radians(270)
    else:   # up
        theta = radians(0)

    r = 8        
    fill(0, 255, 0)
    stroke(0)
    pushMatrix()
    translate(spriteXY.x, spriteXY.y)
    rotate(theta)
    beginShape(PConstants.TRIANGLES)
    vertex(0, -r*2)
    vertex(-r, r)
    vertex(r, r)
    endShape()
    popMatrix()

def drawDestination():
    if (destinationSet == False):
        print("Destination is not set")
        return

    fill(255, 0, 0)
    ellipse(destinationXY.x, destinationXY.y, 15, 15)
    
 
def display(grid=True):
    if (animStart):
        if (len(commands) !=0):
            if (commands[0][0] == mForward):
                __move(mForward, commands[0][1])
            elif (commands[0][0] == mBackward):
                __move(mBackward, commands[0][1])
        
    background(220)
    if (grid):
        showGrid(index=True)
    drawRoads()
    drawDestination()
    drawSprite()

def turnRight(amount = 90):
    commands.append((tRight, amount))
    orgCommands.append((tRight, amount))

def turnLeft(amount = 90):
    commands.append((tLeft, amount))
    orgCommands.append((tLeft, amount))
    
def __turn(type = tRight, amount = 90):
    global spriteLoc, targetDir, targetSet, turnSpeed
    if (targetSet):
        updateSprite()
    else:
        if (type == tRight):
            turnSpeed = abs(turnSpeed)
        if (type == mLeft):
            turnSpeed = -1 * abs(turnSpeed)
            amount *= -1
            
        targetLoc = spriteLoc.get()
        if (spriteDir == dirRight):
            targetLoc.x += amount
        elif (spriteDir == dirBottom):
            targetLoc.y += amount
        elif (spriteDir == dirLeft):
            targetLoc.x -= amount
        else:
            targetLoc.y -= amount
            
        targetXY = gridToXY(targetLoc)
        targetSet = True

    
def moveForward(amount = 3):
    commands.append((mForward, amount))
    orgCommands.append((mForward, amount))
    
def moveBackward(amount = 3):
    commands.append((mBackward, amount))
    orgCommands.append((mBackward, amount))

def __move(type = mForward, amount = 3):
    """ return True if the move forward is done, otherwise return false"""
    global spriteLoc, targetLoc, targetXY, targetSet, speed
    if (targetSet):
        updateSprite()
    else:
        if (type == mForward):
            speed = abs(speed)
        if (type == mBackward):
            speed = -1 * abs(speed)
            amount *= -1
            
        targetLoc = spriteLoc.get()
        if (spriteDir == dirRight):
            targetLoc.x += amount
        elif (spriteDir == dirBottom):
            targetLoc.y += amount
        elif (spriteDir == dirLeft):
            targetLoc.x -= amount
        else:
            targetLoc.y -= amount
            
        targetXY = gridToXY(targetLoc)
        targetSet = True

        
# Renders a vector object 'v' as an arrow and a position 'loc'
def drawVector(v, pos, scayl):
    pushMatrix()
    arrowsize = 6
    # Translate to position to render vector
    translate(pos.x, pos.y)
    stroke(0)
    strokeWeight(2)
    # Call vector heading function to get direction (pointing up is a heading of 0)
    rotate(v.heading2D())
    # Calculate length of vector & scale it to be bigger or smaller if necessary
    len = v.mag()*scayl
    # Draw three lines to make an arrow 
    line(0, 0, len, 0)
    line(len, 0, len-arrowsize, +arrowsize/2)
    line(len, 0, len-arrowsize, -arrowsize/2)
    popMatrix()
