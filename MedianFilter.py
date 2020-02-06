import numpy
from PIL import Image
import numpy as np

def median_filter1(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = numpy.zeros((len(data),len(data[0])))
    for i in range(len(data)):
        for j in range(len(data[0])):
            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])
            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final

def main1():
    img = Image.open("original_chart.png").convert("L")
    arr = numpy.array(img)
    removed_noise = median_filter1(arr, 5 )
    img2 = Image.fromarray(removed_noise)
    img2.show()
    #img2.save( "advancedfilter.png" )

def median_filter(data, filter_size, pos200 , pos150 , pos100 , pos50 ):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = numpy.zeros((len(data),len(data[0])))
    s200 = set([(x, y) for x, y in pos200])
    s150 = set([(x, y) for x, y in pos150])
    s100 = set([(x, y) for x, y in pos100])
    s50 = set([(x, y) for x, y in pos50])
    counttatol = 0
    countin = 0
    countout = 0
    testnum = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            #print( i,j )
            counttatol+=1
            if (i, j) in s50:
                strfinal = "process" + str(i) + " " + str(j) + " value " + str(data[i][j]) + "\n"
                for z in range(filter_size):
                    if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                        for c in range(filter_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(filter_size):
                                if (i + z - indexer, j + k - indexer ) in s200:
                                    strfinal += "\t" +  str( i + z - indexer) + " " + str(j + k - indexer) + " "  + str(data[i + z - indexer][j + k - indexer])  + " in200\n"
                                    #temp.append(data[i + z - indexer][j + k - indexer] // 4)
                                elif (i + z - indexer, j + k - indexer ) in s150:
                                    v = data[i + z - indexer][j + k - indexer] /3
                                    temp.append(v)
                                    strfinal += "\t" +  str( i + z - indexer) + " " + str(j + k - indexer) + " "  + str(data[i + z - indexer][j + k - indexer])  + " in150 insert " +  str(v) + "\n"
                                elif (i + z - indexer, j + k - indexer ) in s100:
                                    v = data[i + z - indexer][j + k - indexer] /2
                                    temp.append(v)
                                    strfinal += "\t" +  str( i + z - indexer) + " " + str(j + k - indexer) + " "  + str(data[i + z - indexer][j + k - indexer])  + " in100 insert " +  str(v) + "\n"
                                    #print( "100" )
                                    #temp.append(data[i + z - indexer][j + k - indexer] // 2)
                                elif (i + z - indexer, j + k - indexer ) in s50:
                                    v = data[i + z - indexer][j + k - indexer] *2/3
                                    temp.append(v)
                                    strfinal += "\t" +  str( i + z - indexer) + " " + str(j + k - indexer) + " "  + str(data[i + z - indexer][j + k - indexer])  + " in50 insert " +  str(v) + "\n"
                                else:
                                    v = data[i + z - indexer][j + k - indexer]
                                    temp.append(v)
                                    strfinal += "\t" +  str( i + z - indexer) + " " + str(j + k - indexer) + " "  + str(data[i + z - indexer][j + k - indexer])  + " normal " +  str(v) + "\n"
                                    #print( "other" , data[i + z - indexer][j + k - indexer]  )
                #print( "before" )
                #print( temp )
                #print( strfinal )                
                #temp.sort()
                #print( "after" )
                #print( temp )
                if( len(temp)  > 2 ):
                    #if( data[i][j] > temp[len(temp) // 2]  ):
                    if( data[i][j] > sum(temp) / len(temp)  ):
                        data_final[i][j] = sum(temp) / len(temp)
                    else:
                        data_final[i][j] = data[i][j]
                else:
                    #data_final[i][j] = data[i][j]
					data_final[i][j] = 0
                countin+=1
                temp = []
                #print( "final" )
                #print( i , j , data[i][j] , data_final[i][j] )
                
            else:
                countout+=1
                data_final[i][j] = data[i][j]
    print( counttatol , countin , countout )
    return data_final
    
    
def main():
    #im1 = Image.open("cali.png").convert("L")
    #im2 = im1.crop((500, 500, 600, 600) )
    #im2.save( 'aaa' ,  'PNG') 
    #imgcal = Image.open("cali_small.png").convert("L")
    imgcal = Image.open("cali.png").convert("L")
    #imgcal = Image.open("original_chart.png").convert("L")
    # imgcal.show()
    np.save("test.npy" , imgcal)
    variance = np.load("test.npy")
    print( variance.shape )
    # variance.shape[0]*variance.shape[1]
    pos250 = np.c_[np.where(variance >= 250)].tolist()
    pos200 = np.c_[np.where(variance >= 200)].tolist()
    pos150 = np.c_[np.where(variance >= 150)].tolist()
    pos100 = np.c_[np.where(variance >= 100)].tolist()
    pos50 = np.c_[np.where(variance > 50)].tolist()
    a = 100.000
    print( a*len(pos250) / (variance.shape[0]*variance.shape[1])  )
    print( a*len(pos200) / (variance.shape[0]*variance.shape[1])  )
    print( a*len(pos150) / (variance.shape[0]*variance.shape[1])  )
    print( a*len(pos100) / (variance.shape[0]*variance.shape[1])  )
    print( a*len(pos50) / (variance.shape[0]*variance.shape[1])  )
    #img = Image.open("cali.png").convert("L")
    #img = Image.open("cali_small.png").convert("L")
    #img = Image.open("original_doll.png").convert("L")
    img = Image.open("original_chart.png").convert("L")
    arr = numpy.array(img)
    #removed_noise = median_filter1(arr, 6 ) 
    #img = Image.fromarray(removed_noise)
    #img.show()
    #removed_noise.save( "basicfilter.png" )
    removed_noise = median_filter(arr, 3, pos200 , pos150  , pos100 , pos50  ) 
    img2 = Image.fromarray(removed_noise)
    img2.show()
    #img.save( "advancedfilter.png" )


main()