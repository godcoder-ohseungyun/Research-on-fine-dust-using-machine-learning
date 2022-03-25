

import os 


class FileMaker:

    root = 'dataFrames/'

    def createDirectory(self,directory): 

        dir = FileMaker.root + directory

        try: 
            if not os.path.exists(dir): 
                os.makedirs(dir) 

        except OSError: 
            print("Error: Failed to create the directory.")



    


