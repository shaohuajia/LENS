
# coding: utf-8

import csv
import os
import sys
import numpy as np

def csv_reader_gaze(filePath):
    
    path = filePath
    #hash table
    fixations = []
    duration = []
    count = 0
    fixations_seq = []
    duration_seq = []
    subjects_seq = []
    length_seq = []
    block_seq = []
    image_seq = []
    
    res = {}
    cnt = 0
    sub = '126'
    img = '43'
    blk = 'dash'

    with open(path) as f:
        f_csv = csv.DictReader(f)
        
        for row in f_csv:
            count += 1
            if((row['Subject']==sub) & (row['Image']==img) & (row['Block']==blk)):
                cnt += 1
                fixations.append((float(row['X']),float(row['Y'])))
                duration.append(int(row['Duration']))
                if(count == 80212):
                    fixations_seq.append(fixations)
                    duration_seq.append(duration)
                    subjects_seq.append(sub)
                    length_seq.append(cnt)
                    block_seq.append(blk)
                    image_seq.append(int(img))
                    #res = {'subject':subjects_seq, 'block':block_seq, 'image':image_seq,
                           #'fixations':fixations_seq , 'duration':duration_seq, 'length':length_seq, }
            else:           
                fixations_seq.append(fixations)
                duration_seq.append(duration)
                subjects_seq.append(sub)
                length_seq.append(cnt)
                block_seq.append(blk)
                image_seq.append(int(img))
                #res = {'subject':subjects_seq, 'block':block_seq, 'image':image_seq,
                       #'fixations':fixations_seq , 'duration':duration_seq, 'length':length_seq, }
                fixations = []
                duration = []
                fixations.append((float(row['X']),float(row['Y'])))
                duration.append(int(row['Duration']))
                sub = row['Subject']
                img = row['Image']
                blk = row['Block']
                cnt = 1
    # Here, the dictionary variable res is kind of a pointer(address), when it is passed to another variable
    # the address is copied instead of the contents
    res = {'Subject':subjects_seq, 'Block':block_seq, 'ImgNumber':image_seq,
           'Fixations':fixations_seq , 'Duration':duration_seq, 'Length':length_seq}
    return res

def csv_reader_img(filepath):
    
    path = filepath
    block = []
    imgNumber = []
    location = []
    res = {}
    
    with open(path) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            block.append(row['Block'])
            imgNumber.append(int(row['ImgNumber']))
            sixteenth_x = ((float(row['axMax']) - float(row['axMin']))/16.0)
            sixteenth_y = ((float(row['ayMax']) - float(row['ayMin']))/16.0)
            location.append(((float(row['axMin'])),(float(row['axMax'])),(float(row['ayMin'])),(float(row['ayMax'])),
                            (float(row['bxMin'])),(float(row['bxMax'])),(float(row['byMin'])),(float(row['byMax'])),
                            (sixteenth_x), (sixteenth_y)))
                                
    res = {'Block':block, 'ImgNumber':imgNumber, 'Location':location}
    #print (res['Location'])
    return res

def gaze_to_fmap (csv_gaze, csv_imgDim):
    
    cnt = 0
    cnt1 = 80
    x = 0
    y = 0
    fmap_seq = []
    # iterate fixation sequences
    for i in range(len(csv_gaze['Fixations'])):
        #for dash images
        if csv_gaze['Block'][i] == 'dash':
            # iterate fixations for a single subject and a single image
            fmap = []
            for j in range(csv_gaze['Length'][i]):
                # determine the fixation to be in imgage a or b
                # in image a
                if ((csv_gaze['Fixations'][i][j][0] > csv_imgDim['Location'][cnt][0]) &
                ((csv_gaze['Fixations'][i][j][0] < csv_imgDim['Location'][cnt][1])) &
                ((csv_gaze['Fixations'][i][j][1] > csv_imgDim['Location'][cnt][2])) &
                ((csv_gaze['Fixations'][i][j][1] < csv_imgDim['Location'][cnt][3])) ):
                    # compute how many units (sixteenth) does this fixation consist
                    x = int(np.floor((csv_gaze['Fixations'][i][j][0] - csv_imgDim['Location'][cnt][0]) / 
                                csv_imgDim['Location'][cnt][8] + 0.5))
                    y = int(np.floor((csv_gaze['Fixations'][i][j][1] - csv_imgDim['Location'][cnt][2]) / 
                                csv_imgDim['Location'][cnt][9] + 0.5))
                    fmap.append((x, y))
                # in image b
                elif ((csv_gaze['Fixations'][i][j][0] > csv_imgDim['Location'][cnt][4]) &
                ((csv_gaze['Fixations'][i][j][0] < csv_imgDim['Location'][cnt][5])) &
                ((csv_gaze['Fixations'][i][j][1] > csv_imgDim['Location'][cnt][6])) &
                ((csv_gaze['Fixations'][i][j][1] < csv_imgDim['Location'][cnt][7])) ):

                    x = int(np.floor((csv_gaze['Fixations'][i][j][0] - csv_imgDim['Location'][cnt][4]) /
                                csv_imgDim['Location'][cnt][8] + 0.5) + 16)
                    y = int(np.floor((csv_gaze['Fixations'][i][j][1] - csv_imgDim['Location'][cnt][6]) / 
                                csv_imgDim['Location'][cnt][9] + 0.5))
                    fmap.append((x, y))
                    
            fmap_seq.append(fmap)        
            cnt += 1
            if cnt >= 79:
                cnt = 0
        #for ball images
        elif csv_gaze['Block'][i] == 'ball':
            # iterate fixations for a single subject and a single image
            fmap = []
            for j in range(csv_gaze['Length'][i]):
                # determine the fixation to be in imgage a or b
                # in image a
                if ((csv_gaze['Fixations'][i][j][0] > csv_imgDim['Location'][cnt][0]) &
                ((csv_gaze['Fixations'][i][j][0] < csv_imgDim['Location'][cnt][1])) &
                ((csv_gaze['Fixations'][i][j][1] > csv_imgDim['Location'][cnt][2])) &
                ((csv_gaze['Fixations'][i][j][1] < csv_imgDim['Location'][cnt][3])) ):
                    # compute how many units (sixteenth) does this fixation consist of
                    x = int(np.floor((csv_gaze['Fixations'][i][j][0] - csv_imgDim['Location'][cnt][0]) / 
                                csv_imgDim['Location'][cnt][8] + 0.5))
                    y = int(np.floor((csv_gaze['Fixations'][i][j][1] - csv_imgDim['Location'][cnt][2]) / 
                                csv_imgDim['Location'][cnt][9] + 0.5))
                    fmap.append((x, y))
                # in image b
                elif ((csv_gaze['Fixations'][i][j][0] > csv_imgDim['Location'][cnt][4]) &
                ((csv_gaze['Fixations'][i][j][0] < csv_imgDim['Location'][cnt][5])) &
                ((csv_gaze['Fixations'][i][j][1] > csv_imgDim['Location'][cnt][6])) &
                ((csv_gaze['Fixations'][i][j][1] < csv_imgDim['Location'][cnt][7])) ):

                    x = int(np.floor((csv_gaze['Fixations'][i][j][0] - csv_imgDim['Location'][cnt][4]) /
                                csv_imgDim['Location'][cnt][8] + 0.5) + 16)
                    y = int(np.floor((csv_gaze['Fixations'][i][j][1] - csv_imgDim['Location'][cnt][6]) / 
                                csv_imgDim['Location'][cnt][9] + 0.5))
                    fmap.append((x, y))
                    
            fmap_seq.append(fmap)        
            cnt += 1
            if cnt >= 159:
                cnt = 80
        # error                
        else:
            print('----error----: unsurported format')
    fmap_dic = {'Fmap': fmap_seq}        
    csv_gaze.update(fmap_dic)
    return csv_gaze