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
            os.mkdir(name)
            for grouping in sizeable:
                for path in grouping:
                    if name in path:
                        shutil.copy(os.getcwd()+"\\"+path.replace(".\\",""),os.getcwd()+"\\"+name)

    def removeEmptyDirs(self):
        dirs = list(filter(lambda d: '.' not in d ,os.listdir()))
        for f in dirs:
            num_files = len(glob.glob('./'+f))
            print(f, num_files)
            if num_files == 0:
                os.rmdir(f)

    def main(self):
        file_paths = glob.glob('./*')
        files = self.getFiles(file_paths)
        file_names = list(set(self.getFileNames(files)))
        aggregates = self.getAggregates(file_paths, file_names)
        self.makeDirs(file_names, aggregates)
        os.rmdir(os.getcwd()+'\\aggregate')
#        self.removeEmptyDirs()
if __name__ == "__main__":
    AGGREGATOR().main()
    
