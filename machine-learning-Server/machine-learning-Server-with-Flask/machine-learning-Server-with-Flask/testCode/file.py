



import os 


def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 

    except OSError: 
        print("Error: Failed to create the directory.")



createDirectory('C:/Users/afrad/OneDrive/바탕 화면/test/testd')


f = open(r"C:/Users/afrad/OneDrive/바탕 화면/test/testd/{}_DF_{}.txt".format("test",12), 'w')
f.close()