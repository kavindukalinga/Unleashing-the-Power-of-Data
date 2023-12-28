import pandas as pd

class SearchAndQuoteServiceBean:
    data_all=[]
    def __init__(self,name,count,minTime,maxTime,totalTime):

        self.name=name
        self.count=count
        self.minTime=minTime
        self.maxTime=maxTime
        self.totalTime=totalTime

        # Actions to execute
        SearchAndQuoteServiceBean.data_all.append(self)

    def averageTime(self):
        return self.totalTime/self.count
    
    def p_tot_time(self, total_total_time):
        return (self.totalTime / total_total_time) * 100
    
    def p_hits(self, total_hits):
        return (self.count / total_hits) * 100

    @classmethod       
    def fromTxt(cls): 
        with open(file_path, 'r') as file:
            lines = file.readlines()            

        for line in lines[8:16]:
            items=line.split()
            SearchAndQuoteServiceBean(
                name=items[1][6:-1],
                count=int(items[2][7:-1]),
                minTime=int(items[3][9:-1]),
                maxTime=int(items[4][9:-1]),
                totalTime=int(items[5][11:-1]),
            )
    
    def __repr__(self):
        return f"SearchAndQuoteServiceBean('{self.name}',{self.count},{self.minTime},{self.maxTime},{self.totalTime})"

file_path = "/home/kalinga/Documents/ISAintern/Task01/raw_data/data_20231120150040.txt"
SearchAndQuoteServiceBean.fromTxt()
#print(SearchAndQuoteServiceBean.data_all)

# Total_time percentage
total_total_time = sum(methodsOfSearchAndQuoteServiceBean.totalTime for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all)

# hits percentage
total_hits = sum(methodsOfSearchAndQuoteServiceBean.count for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all)

# # Sort instances by AverageTime
# sortedMethodsByCount = sorted(SearchAndQuoteServiceBean.data_all, key=lambda x: x.averageTime())
# result_dict = {methodsOfSearchAndQuoteServiceBean.name: methodsOfSearchAndQuoteServiceBean.averageTime() for methodsOfSearchAndQuoteServiceBean in sortedMethodsByCount}

print("SearchAndQuoteServiceBean")
# Creating a dictionary with sample data
data = {
    'Name': [methodsOfSearchAndQuoteServiceBean.name for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all],
    'AverageTime': [round(methodsOfSearchAndQuoteServiceBean.averageTime(),2) for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all],
    'p_tot_time': [round(methodsOfSearchAndQuoteServiceBean.p_tot_time(total_total_time),2) for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all],
    'p_hits': [round(methodsOfSearchAndQuoteServiceBean.p_hits(total_hits),2) for methodsOfSearchAndQuoteServiceBean in SearchAndQuoteServiceBean.data_all]
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.DataFrame(data) # Dataframe
print(df)
