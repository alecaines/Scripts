'''
Author: Alexander Caines
Description: If multiple files occur with the same name but different file types, aggregate them into
their respective files.
'''

import shutil
import glob 
import os

class AGGREGATOR(object):
    def __init__(self, address):
        self.address = address
    
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
        sans_bars =[list(map(lambda e: e.replace(".\\", ""), grouping)) for grouping in sizeable]
        sizeable_names = [list(map(lambda e: e[:e.index(".")], grouping)) for grouping in sans_bars] 

        for name in file_names:
            if not os.path.exists(self.address+"\\"+name):
                os.mkdir(self.address+"\\"+name)
            for grouping in sizeable:
                for path in grouping:
                    if name+"." in path and os.path.exists(self.address+"\\"+name):
                        if os.path.isfile(self.address+"\\"+name):
                            os.remove(os.path.isfile(self.address+"\\"+name))
                        else:                            
                            shutil.copy(os.getcwd(self.address)+"\\"+path.replace(".\\",""),os.getcwd(self.address)+"\\"+name)
                            os.remove(os.getcwd(self.address)+"\\"+path.replace(".\\", ""))

    def removeEmptyDirs(self):
        dirs = list(filter(lambda d: '.' not in d, os.listdir(self.address)))
        for d in dirs:
            if os.path.isfile(os.getcwd(self.address)+"\\"+d):
                os.remove(os.getcwd(self.address)+"\\"+d)
            elif len(os.listdir(os.getcwd(self.address)+"\\"+d)) == 0:
                os.rmdir(d)

    def pickUpDotUns(self):
        dtdu = list(filter(lambda s: '.tex.un' in s, os.listdir(self.address)))
        dirs = list(filter(lambda s: '.' not in s, os.listdir(self.address)))

        for d in dirs:
            if "."+d+".tex.un~" in dtdu:
                shutil.copy(os.getcwd(self.address)+"\\"+"."+d+".tex.un~", os.getcwd(self.address)+"\\"+d)
                os.remove(os.getcwd(self.address)+"\\"+"."+d+".tex.un~")

    def main(self):
        self.removeEmptyDirs()
        file_paths = []
        if self.address == "":
            file_paths = os.listdir()
            self.address = os.getcwd()
        else:            
            file_paths = os.listdir(self.address)
##        file_paths = glob.glob(self.address)
        files = self.getFiles(file_paths)
        file_names = list(set(self.getFileNames(files)))
        aggregates = self.getAggregates(file_paths, file_names)
        self.makeDirs(file_names, aggregates)
        self.pickUpDotUns()
        self.removeEmptyDirs()

if __name__ == "__main__":
    print("===================AGGREGATE===========================")
    print("Enter the full address of the directory you would\n like to aggregate.\n")
    address = input("Enter the directory you would like to aggregate")
    AGGREGATOR(address).main()
    print("============================================================================")
    print("Files have been succesffully aggregated. Those files which occur in\n multiplicity are moved into folders with their respective filename.\nAll singular files are left without grouping folders.")    

    print("============================================================================")
