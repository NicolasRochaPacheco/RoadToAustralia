import lightnet

path = "../../outputData/frame0.png"


model = lightnet.load('yolo')
image = lightnet.Image.from_bytes( open(path,'rb').read() )
boxes = model( image )

print( boxes )
