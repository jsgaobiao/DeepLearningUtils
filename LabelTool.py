# import the necessary packages
import os
import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
refColor = 0
newColor = 0
NUM_OF_CLASSESS = 9

def ColorMap(data, _img):
    if data[0] == 0:
        data = [0,0,0]
    elif data[0] == 1:        # people
        data = [0,0,255]
    elif data[0] == 2:      # car
        data = [255,0,0]
    elif data[0] == 3:      # tree
        data = [0,255,0]
    elif data[0] == 4:      # sign
        data = [255,0,255]
    elif data[0] == 5:      # building
        data = [255,255,0]
    elif data[0] == 6:      # cyclist
        data = [0,128,255]
    elif data[0] == 7:      # stop bicycle
        data = [128,64,0]
    elif data[0] == 8:      # road
        data = [117,149,208]
    else:
        data = [_img[0], _img[0], _img[0]]
    return data

def MergeImage(_img, _gt):
    height, width, channel = _gt.shape
    for i in range(height):
        for j in range(width):
            # Label color of gt
            _img[i,j] = ColorMap(_gt[i,j], _img[i,j])
    return _img

def replaceColor(gt, pt, color, newColor, newImg, mergeImg):
    for i in range(int(pt[0][1]), min(143,int(pt[1][1]))):
        for j in range(int(pt[0][0]), min(1079,int(pt[1][0]))):
            if (gt[i,j] == color).all():
                gt[i,j] = newColor
                newImg[i,j] = ColorMap(gt[i,j], newImg[i,j])
                mergeImg[i,j] = ColorMap(gt[i,j], mergeImg[i,j])
    return gt, newImg, mergeImg

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, refColor, newColor, image, gt, mergeImg, newImg
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        # draw a rectangle around the region of interestuntil the 'q' key is pressed
        cv2.rectangle(newImg, refPt[0], refPt[1], (0, 255, 0), 2)
        print("rect: " + str(refPt))
    elif event == cv2.EVENT_RBUTTONDOWN:
        refColor = gt[y, x].copy()
        print("refColor: " + str(refColor))
        gt, newImg, mergeImg = replaceColor(gt, refPt, refColor, newColor, newImg, mergeImg)

PATH = '/home/gaobiao/Documents/2-1/ladybug/'     # end with '/'
allImgList = os.listdir(PATH)
imgList = []
gtList = []
mergeImgList = []
for i in allImgList:
    if i.split('_')[1][0] == 'g':
        gtList.append(i)
    elif i.split('_')[1][0] == 'i':
        imgList.append(i)
    elif i.split('_')[1][0] == 'm':
        mergeImgList.append(i)

gtList.sort()
imgList.sort()
mergeImgList.sort()

i = 0
while i < len(imgList):
    imgFileName = PATH + imgList[i]
    gtFileName = PATH + gtList[i]
    mergeImgFileName = PATH + mergeImgList[i]
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(imgFileName)
    gt = cv2.imread(gtFileName, cv2.IMREAD_GRAYSCALE)
    mergeImg = cv2.imread(mergeImgFileName)
    newImg = mergeImg.copy()
    gtClone = gt.copy()
    mergeImgClone = mergeImg.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    # keep looping
    while True:
        # display the image and wait for a keypress
        # cv2.imshow("image", Merge/Image(image, gt))
        cv2.imshow("image", newImg)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            gt = gtClone.copy()
            mergeImg = mergeImgClone.copy()
            newImg = mergeImg.copy()
            cv2.imshow("image", newImg)
            # cv2.imshow("image", MergeImage(image, gt))
        # if the 'c' key is pressed, break from the loop
        elif key == ord("d"):
            break
        elif key == ord("a"):
            if i > 0:
                i -= 2
            break
        elif key == ord(" "):
            cv2.imwrite(imgFileName, image)
            cv2.imwrite(gtFileName, gt)
            cv2.imwrite(mergeImgFileName, mergeImg)
            break
        elif (key >= ord("0")) and (key <= ord("8")):
            newColor = key - ord("0")
            print("newColor : %d\n" % newColor)
        elif key == ord("q"):
            exit(0)
    i += 1

# close all open windows
cv2.destroyAllWindows()
