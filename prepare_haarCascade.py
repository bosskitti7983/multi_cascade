# ~/virtualenv/ROBOTICS_studios/bin


'''*************************************************
*                                                  *
*                  import library                  *
*                                                  *
*************************************************'''

import os
import sys
import platform
from random import choice

from PIL import Image
from math import sqrt, pow
import numpy as np

'''*************************************************
*                                                  *
*                 define valuable                  *
*                                                  *
*************************************************'''

dirCom = '/'
weight=24
height=24
listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six',
                'seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH',
                'SevenTH','EightTH','NineTH']

'''*************************************************
*                                                  *
*                   main library                   *
*                                                  *
*************************************************'''

def main():
    global dirCom, weight, height, listOfClass
    inputKey = sys.argv[1:]
    
    if platform.system() == 'Linux':
        dirCom = '/'
    elif platform.system() == 'Windows':
        dirCom = '\\'
        
    if inputKey == [] or str(inputKey[0]) == 'help':
        print('set data')
        print('prepare_haarCascade [method] [param] \nmethod:\tgen_image\tresize\t\t\tcreate_bg')
        print('param:\tnumber/class\tmain_image -- size\tmain_class\n\t1000\t\ttrain-0 24\t\tone')
        print('------------------------------------------------------------')
        print('generate classification : required --> libopencv-dev ')
        print('prepare_haarCascade [method] [param]')
        print('method:\tcreatesamples\t\ttraincascade\t\t\t\t\thaartraining\tperformance')
        print('param:\tmain_class -- number\tmain_class -- numpos -- numneg -- numstate\tnon_finished\tnon_finished')
        print('\tone 1000\t\tone 800 2400 10\t\t\t\t\t-\t\t-')
        print('------------------------------------------------------------------------------------')
        print('generate 30 classification  : required --> libopencv-dev ')
        print('prepare_haarCascade autogen [param]')
        print('param:\tnumber/class -- main_image -- size -- numstate')
        print('\t 1000 train-0 24 10\n')

    elif str(inputKey[0]) == 'resize':
        try :
            resize_image(selectFile = (str(inputKey[1])+'.png'), size = int(inputKey[2]))

        except Exception :
            resize_image()

    elif str(inputKey[0]) == 'create_bg':
        try :
            create_bg_txt(select_value = str(inputKey[1]))
        except Exception as e:
            sys.exit('error argument : '+str(e))

    elif str(inputKey[0]) == 'gen_image':
        try :
            generate_picture(limitFilePerClass = int(inputKey[1]))
        except Exception as e:
            generate_picture()

    elif str(inputKey[0]) == 'createsamples' and platform.system() == 'Linux' :
        try:
            run_opencv_createsamples(main_class=str(inputKey[1]),number=str(inputKey[2]))
        except Exception as e:
            sys.exit('createsamples argument error : '+str(e))

    elif str(inputKey[0]) == 'traincascade' and platform.system() == 'Linux' :
        if str(inputKey[1]) in str(listOfClass) : 
            try:
                run_opencv_traincascade(main_class=str(inputKey[1]),numpos=str(inputKey[2]),numneg=str(inputKey[3]),numstate=str(inputKey[4]))
            except Exception as e:
                sys.exit('traincascade argument error : '+str(e))
        else :
            sys.exit('out of class')

    elif str(inputKey[0]) == 'haartraining' and platform.system() == 'Linux' :
        sys.exit('this method not finished\nPlease run prepare_haarCascade.py help')

    elif str(inputKey[0]) == 'performance' and platform.system() == 'Linux' :
        sys.exit('this method not finished\nPlease run prepare_haarCascade.py help')

    elif str(inputKey[0]) == 'autogen' and platform.system() == 'Linux' :
        try :
            AutoGenerateClassification(numberPerClass=str(inputKey[1]), main_img=str(inputKey[2]), size=str(inputKey[3]), numstate=str(inputKey[4]))
        except Exception as e:
            sys.exit('error:'+str(e))
    else :
        sys.exit("method doesn't have in program\n-----------------------\nPlease run prepare_haarCascade.py help")


'''*************************************************
*                                                  *
*                    sub module                    *
*                                                  *
*************************************************'''

def generate_picture(limitFilePerClass = 50):
    '''generate picture from file in folder dataCompress and save to folder
    dataExtract with limit picture per class.'''

    '''*************************************************
    *                                                  *
    *              config generate number              *
    *                                                  *
    *************************************************'''
    numCount = 0
    numKeep = 0
    

    '''*************************************************
    *                                                  *
    *                   prepare data                   *
    *                                                  *
    *************************************************'''

    suffix = ['test','train','validate']
    listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six',
                        'seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH',
                        'SevenTH','EightTH','NineTH']

    '''*************************************************
    *                                                  *
    *                   remove old data                *
    *                                                  *
    *************************************************'''
    try:
        fileList= [f for f in os.listdir('dataExtract')]
        for f in fileList:
            os.remove(os.path.join('dataExtract',f)) 

    except Exception:
        print("error to remove file in dataExtract folder")

    '''*************************************************
    *                                                  *
    *              read & generate data                *
    *                                                  *
    *************************************************'''

    for s in range(1,3): # traain & validate
        for j in range(0,30): # 30 class
            object = listOfClass[j]
            f = open('dataCompress'+dirCom+'dataset_'+str(object)+'_all_'+suffix[s]+'.txt','r')
            image = str(f.read()).split('\n')[:-1]
            f.close()

            numKeep += numCount
            numCount = 0
            for i in range(len(image)):
                
                path = 'dataExtract'+dirCom+str(object)+'_'+suffix[s]+'-'+str(numCount)+'.png'

                image[i] = np.fromstring(image[i], dtype=float, sep=',')
                image[i] = np.array(image[i])
                image[i] = np.reshape(image[i],(int(sqrt(len(image[i]))),int(sqrt(len(image[i])))))

                img = Image.fromarray((image[i]*255).astype(np.uint8))
                img.save(path)

                if numCount > int(limitFilePerClass)-1 :
                    break
                if (numCount%int(int(limitFilePerClass)/2)) == 0 :
                    print("generate"+str(numKeep+numCount)+ ":"+suffix[s]+'-'+str(object) +"-"+str(numCount))

                numCount+=1

def resize_image(selectFile = 'test-0.png', size = 24):
    '''resize image from folder dataExtract and save to folder data, 
        And select main image.'''

    print('select file *'+selectFile +" : " +str(size))        

    '''*************************************************
    *                                                  *
    *                   remove old data                *
    *                                                  *
    *************************************************'''
    try:
        fileList= [f for f in os.listdir('data')]
        for f in fileList:
            os.remove(os.path.join('data',f)) 
    except Exception:
        print("error to remove file in data folder")

    try:
        fileList= [f for f in os.listdir('main_img')]
        for f in fileList:
            os.remove(os.path.join('main_img',f)) 
    except Exception:
        print("error to remove file in main_img folder")

    '''*************************************************
    *                                                  *
    *            resize and select main image          *
    *                                                  *
    *************************************************'''

    path = 'dataExtract'
    fileList= [f for f in os.listdir(path)]

    for f in fileList:
        img = Image.open(path+dirCom+f)
        if img.height < int(size):
            sys.exit('size is bigger than '+str(img.height))

        img = img.resize((int(size),int(size)),Image.ANTIALIAS)
        img.save('data'+dirCom+f)

        if f.split('_')[1] == selectFile:
            img.save('main_img'+dirCom+f)


def create_bg_txt(select_value):
    '''use image from dataExtract and input string to write bg_neg.txt and bg_pos.txt .'''
    
    '''*************************************************
    *                                                  *
    *            remove & create old file              *
    *                                                  *
    *************************************************'''

    if os.path.isfile('bg_pos.txt') :
        os.remove('bg_pos.txt')
    if os.path.isfile('bg_neg.txt') :
        os.remove('bg_neg.txt')

    f_pos = open("bg_pos.txt","w+")
    f_neg = open("bg_neg.txt","w+")
    
    '''*************************************************
    *                                                  *
    *                 random data list                 *
    *                                                  *
    *************************************************'''
    
    listData = os.listdir('data')
    randomList = []
    while len(listData) > 0 :
        randomData = choice(listData)
        randomList.append(randomData)
        listData.remove(randomData)    
 
    '''*************************************************
    *                                                  *
    *            split positive and negative           *
    *                                                  *
    *************************************************'''


    countPos =0
    countNeg =0
    if str(select_value) in str(listOfClass):
        for f in randomList:
            if str(f.split('_')[0]) == str(select_value):
                f_pos.write("data"+dirCom+f+"\n")
                countPos+=1
            else:
                f_neg.write("data"+dirCom+f+"\n")
                countNeg+=1
    else:
        sys.exit('out of class')
    
    print("number of positive : "+str(countPos))
    print("number of negative : "+str(countNeg))



def run_opencv_createsamples(main_class='',number=''):
    ''' opencv_createsamples library from libopencv-dev .\n
        To generate vector file for run opencv_traincascade .'''

    if main_class=='' or number=='':
        sys.exit('main class or number is invalid')

    command = 'opencv_createsamples -img main_img'+dirCom+str(main_class)+'* -bg bg_pos.txt -vec positives.vec -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1 -num '+str(number)
    os.system(command)

def run_opencv_traincascade(main_class,numpos,numneg,numstate):
    ''' opencv_traincascade library from libopencv-dev .\n
        To generate haarCascade classification file. '''

    if numpos==0 or numneg==0 or numstate==0 :
        sys.exit('numpos | numneg | numstate is 0')
    
    command = 'opencv_traincascade -data output_data'+dirCom+str(main_class) +dirCom +' -vec positives.vec -bg bg_neg.txt -numPos '+str(numpos)+' -numNeg '+str(numneg)+' -numStages '+str(numstate)+' -w '+str(weight)+' -h '+str(height)+' -precalcValBufSize 4096 -precalcIdxBufSize 4096'
    os.system(command)

def run_opencv_haartraining():
    '''Now, don't know how it use.'''
    
    pass

def run_opencv_performance():
    '''Now, don't know how it use.'''
        
    pass

def AutoGenerateClassification(numberPerClass=1000, main_img='train-0',size=24, numstate=10):
    '''auto generate 30 classification by auto parameter.'''
    print('gen_image '+str(numberPerClass)+' per class')
    generate_picture(limitFilePerClass = numberPerClass)
    print('done')
    resize_image(selectFile=str(main_img)+'.png',size=size)
    
    for selectClass in listOfClass:
        create_bg_txt(select_value=selectClass)
        
        with open('bg_neg.txt','r') as f :
            countNeg = len(str(f.read()).split('\n'))
        with open('bg_pos.txt','r') as f :
            countPos = len(str(f.read()).split('\n'))

        num = predictNumPosNumNeg(countPos=countPos,countNeg=countNeg)    

        run_opencv_createsamples(main_class=selectClass,number=int(num[0]))
        run_opencv_traincascade(main_class=selectClass,numpos=int(num[0]*3/4),numneg=int(num[0]*9/4),numstate=int(numstate))


def predictNumPosNumNeg(countPos,countNeg):
    ''' find NumPos and NumNeg in term i*pow(10,n) .'''
    countKeep = 0
    pos = countPos
    neg = countNeg
    while pos >= 10:
        pos /= 10
        countKeep+=1
    pos = pow(10,countKeep)*pos

    countKeep = 0
    while neg >= 10:
        neg /= 10
        countKeep+=1
    neg = pow(10,countKeep)*neg
    
    return [pos,neg]

if __name__ == '__main__':
    main()