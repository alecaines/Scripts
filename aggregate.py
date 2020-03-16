'''
Author: Alexander Caines
Description: If multiple files occur with the same name but different file types, aggregate them into
their respective files.
'''
import shutil
import glob 
import os

class AGGREGATOR(object):
    def __init__(self):
        pass
    
    def getFiles(self, file_paths):
        return [file_paths[i].replace(".\\", "") for i in range(len(file_paths))] 

    def getFileNames(self, files):
        files = list(filter(lambda f: '.' in f, files))        
        return [e[:e.index('.')] for e in files]
    
    def getAggregates(self, file_paths, file_names):
        first_pass = [[path if name+'.' in path else None for path in file_paths] for name in file_names]
        second_pass = [list(filter((None).__ne__, group)) for group in first_pass]
        return second_pass
    
    def makeDirs(self, file_names, aggregates):
        sizeable = list(filter(lambda agg: len(agg) > 1, aggregates))       
        for name in file_names:
            if not os.path.exists(name):
                os.mkdir(name)
            for grouping in sizeable:
                for path in grouping:
                    if name in path and os.path.exists(os.getcwd()+"\\"+path.replace(".\\","")):
                        shutil.copy(os.getcwd()+"\\"+path.replace(".\\",""),os.getcwd()+"\\"+name)
                        os.remove(os.getcwd()+"\\"+path.replace(".\\", ""))

    def removeEmptyDirs(self):
        dirs = list(filter(lambda d: '.' not in d, os.listdir()))
        for d in dirs:
            if len(os.listdir(os.getcwd()+"\\"+d)) == 0:
                os.rmdir(d)

    def pickUpDotUns(self):
        dtdu = list(filter(lambda s: '.tex.un' in s, os.listdir()))
        dirs = list(filter(lambda s: '.' not in s, os.listdir()))
        for dr in dirs:
            for tu in dtdu:
                if dr in tu:
                    shutil.copy(os.getcwd()+"\\"+tu.replace(".\\",""),os.getcwd()+"\\"+dr)
                    os.remove(os.getcwd()+"\\"+tu.replace(".\\",""))

    def main(self):
        file_paths = glob.glob('./*')
        files = self.getFiles(file_paths)
        file_names = list(set(self.getFileNames(files)))
        aggregates = self.getAggregates(file_paths, file_names)
        self.makeDirs(file_names, aggregates)
        self.pickUpDotUns()
        self.removeEmptyDirs()

if __name__ == "__main__":
    AGGREGATOR().main()
    
