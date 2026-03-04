
class Descriptive():
    
    def init(self):
        pass
       
    def quanqual(self,dataset):
        Quantitative=[]
        Qualitative=[]

        for column in dataset.columns:
            if(dataset[column].dtype=="object"):
                Qualitative.append(column)
            else:
                Quantitative.append(column)
        return Quantitative,Qualitative
    
    