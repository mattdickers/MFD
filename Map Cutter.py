import PIL.Image as PIL
from tkinter import *
from tkinter.filedialog import *

level= 2

root = Tk()
root.geometry("0x0+0+0")
root.overrideredirect(True)
imagePath = askopenfilename(title="Select Image to Cut:"
                       ,filetypes=(("PNG files","*.png"),("All files","*")))
print(imagePath)

folderPath = askdirectory()

root.destroy()

image = PIL.open(imagePath)
width = image.size[0]
height = image.size[1]

levelsDict = {0:[2,1,2,1,0],1:[4,2,4,2,1],2:[8,4,8,4,3]}

for column in range(levelsDict[level][0]):
    for row in range(levelsDict[level][1]):
        newImage = image.crop((column*width/levelsDict[level][2],row*height/levelsDict[level][3],column*width/levelsDict[level][2]+width/levelsDict[level][2],row*height/levelsDict[level][3]+height/levelsDict[level][3]))
        newImage = newImage.resize((256,256))
        name = str(column)+"_"+str(levelsDict[level][4]-row)
        newImage.save(folderPath+"\\"+name+".png")
