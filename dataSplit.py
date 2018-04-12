'''
    Split the data and labels into 'train' 'test' 'val'.
    Generate file list into 'train.txt' 'test.txt' 'val.txt'
'''

from sklearn.cross_validation import train_test_split
import os
import shutil

PATH = '/home/gaobiao/Documents/KittiSeg/DATA/ladybug/'     # end with '/'
TRAIN_FILE = '/home/gaobiao/Documents/KittiSeg/DATA/train.txt'
TEST_FILE = '/home/gaobiao/Documents/KittiSeg/DATA/test.txt'
VAL_FILE = '/home/gaobiao/Documents/KittiSeg/DATA/val.txt'
f_train = open(TRAIN_FILE, 'w')
f_test = open(TEST_FILE, 'w')
f_val = open(VAL_FILE, 'w')

data = []
label = []
listName = os.listdir(PATH)

for fileName in listName:
    if fileName[-6:-4] != 'gt':
        data.append(fileName)
    else:
        label.append(fileName)

data.sort()
label.sort()

X_trainval, X_test, Y_trainval, Y_test = train_test_split(data, label, test_size=0.2)
X_train, X_val, Y_train, Y_val = train_test_split(X_trainval, Y_trainval, test_size=0.2)

os.mkdir(PATH + 'train')
os.mkdir(PATH + 'train_gt')
os.mkdir(PATH + 'test')
os.mkdir(PATH + 'test_gt')
os.mkdir(PATH + 'val')
os.mkdir(PATH + 'val_gt')
for i in range(len(X_train)):
    shutil.copy2(PATH + X_train[i], PATH + 'train/' + X_train[i])
    shutil.copy2(PATH + Y_train[i], PATH + 'train_gt/' + Y_train[i])
    f_train.write(PATH + 'train/' + X_train[i] + ' ' + PATH + 'train_gt/' + Y_train[i] + '\n')
for i in range(len(X_test)):
    shutil.copy2(PATH + X_test[i], PATH + 'test/' + X_test[i])
    shutil.copy2(PATH + Y_test[i], PATH + 'test_gt/' + Y_test[i])
    f_test.write(PATH + 'test/' + X_test[i] + ' ' + PATH + 'test_gt/' + Y_test[i] + '\n')
for i in range(len(X_val)):
    shutil.copy2(PATH + X_val[i], PATH + 'val/' + X_val[i])
    shutil.copy2(PATH + Y_val[i], PATH + 'val_gt/' + Y_val[i])
    f_val.write(PATH + 'val/' + X_val[i] + ' ' + PATH + 'val_gt/' + Y_val[i] + '\n')

f_train.close()
f_test.close()
f_val.close()