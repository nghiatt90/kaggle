import pandas as pd
import matplotlib.pyplot as plt
import re

# pd.set_option('max.rows', 6)

input_file = 'train.csv'
rawdata = pd.read_csv(
    input_file,
    index_col=0,
    usecols=lambda col: col not in ['Ticket', 'Cabin', 'Embarked'],
    dtype={
        'Pclass': 'category'
    }
)

labels = rawdata['Survived']
rawdata.__delitem__('Survived')


def process_name(name):
    pattern_str = '.*,\s([A-Za-z]*\.).*'
    m = re.match(pattern_str, name)
    if m is not None:
        return m.group(1)
    print 'Name is None: {}'.format(name)

name_honor = rawdata['Name'].map(process_name)
print name_honor



#plt.boxplot(rawdata['Pclass'])
#print rawdata['Pclass'].describe()
#plt.show()
#print rawdata


