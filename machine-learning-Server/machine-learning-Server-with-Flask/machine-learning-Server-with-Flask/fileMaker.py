

import os 


class FileMaker:

    root = 'C:/Users/afrad/OneDrive/문서/Research-on-fine-dust-using-machine-learning/machine-learning-Server/machine-learning-Server-with-Flask/machine-learning-Server-with-Flask/dataFrames/'

    def createDirectory(self,directory): 

        dir = FileMaker.root + directory

        try: 
            if not os.path.exists(dir): 
                os.makedirs(dir) 

        except OSError: 
            print("Error: Failed to create the directory.")



    


