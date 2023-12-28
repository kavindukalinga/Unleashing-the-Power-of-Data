import re
import pandas as pd

class DataProcessing:
    COLUMN_NAMES = ['beanName', 'methodName', 'count', 'minTime', 'maxTime', 'totalTime']
    BEAN_PATTERN = re.compile(r"jboss.j2ee:ear=(.*?),jar=(.*?),name=(.*?),service=EJB3")
    METHOD_PATTERN = re.compile(r"<method name='(.*?)' count='(.*?)' minTime='(.*?)' maxTime='(.*?)' totalTime='(.*?)' />")

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_bean_name(self, line):
        match = self.BEAN_PATTERN.search(line)
        return match.group(3) if match else None

    def extract_method_info(self, line):
        match = self.METHOD_PATTERN.search(line)
        return {
            'methodName': match.group(1),
            'count': int(match.group(2)),
            'minTime': int(match.group(3)),
            'maxTime': int(match.group(4)),
            'totalTime': int(match.group(5)),
        } if match else None

    def get_data_frame(self):
        data_list = []
        current_bean_name = None

        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith('jboss'):
                    current_bean_name = self.extract_bean_name(line)
                elif line.startswith('<method'):
                    method_info = self.extract_method_info(line)
                    if current_bean_name and method_info:
                        method_info['beanName'] = current_bean_name
                        data_list.append(method_info)

        return pd.DataFrame(data_list, columns=self.COLUMN_NAMES)

    def mean(self, field):
        return self.get_data_frame()[field].mean()

    def standard_deviation(self, field):
        return self.get_data_frame()[field].std()


if __name__ == "__main__":
    file_path = "./raw_data/data_20231120150040.txt"
    data_processor = DataProcessing(file_path)

    print("Mean of 'minTime':", data_processor.mean('minTime'))
    print("Standard Deviation of 'count':", data_processor.standard_deviation('count'))
    print("DataFrame:")
    print(data_processor.get_data_frame().head())
