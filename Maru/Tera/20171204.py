
# coding: utf-8

# In[11]:


import re
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt


# In[12]:


labels = ['WT', 'SF', 'BT', 'PR', 'PF', 'M1', 'M2', 'M3', 'M4', 'M5', 'IO', 'IS', 'IC', 'CO', 'CC', 'CP', 'CS', 'F1',
          'F2', 'FD', 'MD', 'TP']
date_str = ''


# In[13]:


def get_df(col, orig):
    ret = pd.DataFrame({'time': orig['time'], col: orig[col]})
    ret = ret.set_index('time')
    return ret.dropna()


# In[14]:


def process_line(m):
    time = datetime.datetime.strptime(date_str + ' ' + m.group(1)[:-4], '%Y%m%d %H:%M:%S')
    code = m.group(2)
    value = m.group(3)
    return [time, code, float(value)]


# In[15]:


def process_line2(m):
    time = datetime.datetime.strptime(date_str + ' ' + m.group(1)[:-4], '%Y%m%d %H:%M:%S')
    code = m.group(2)
    params = m.group(3).split(',')
    sensor = params[0]
    values = [int(x[x.find(':') + 1:]) for x in params[1:]]
    values = {labels[i]: values[i] for i in range(len(labels))}
    return time, code, sensor, values


# In[16]:


def process_file(input_file):
    pattern_str1 = '([0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9]*).*\"(SO#70[0-9][0-9])\[([0-9]*)(g|h|ms|s|sec|A).*].*"'
    pattern1 = re.compile(pattern_str1)
    pattern3 = "[0-9]{8}"
    pattern3_str3 = re.compile(pattern3)
    m = pattern3_str3.search(input_file)
    global date_str
    if m:
        date_str = m.group(0)

    all_data1 = []
    with open(input_file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            m1 = pattern1.match(line)
            if m1 is not None:
                all_data1.append(process_line(m1))
    df = pd.DataFrame(all_data1, columns=['time', 'code', 'value'])
    new_df = pd.DataFrame({'time': df['time'], 'Infeed shutter open': df['value'].where('SO#7002' == df['code']),
                           'Infeed shutter close': df['value'].where('SO#7003' == df['code']),
                           'Infeed shutter close. delay mode': df['value'].where('SO#7004' == df['code']),
                           'Compactor shutter open': df['value'].where('SO#7005' == df['code']),
                           'Compactor shutter close': df['value'].where('SO#7006' == df['code']),
                           'Compactor move delay': df['value'].where('SO#7007' == df['code']),
                           'Bottle weight': df['value'].where('SO#7008' == df['code']),
                           'Cleaning time.': df['value'].where('SO#7009' == df['code']),
                           'Inverter operating time': df['value'].where('SO#7012' == df['code']),
                           'Inverter current peak/Reset/60Hz': df['value'].where('SO#7013' == df['code']),
                           'Inverter current peak/Reset/75Hz': df['value'].where('SO#7014' == df['code']),
                           'Inverter current peak/60Hz': df['value'].where('SO#7015' == df['code']),
                           'Inverter current peak/75Hz': df['value'].where('SO#7016' == df['code']),
                           'Weight peak/Reset': df['value'].where('SO#7017' == df['code']),
                           'Weight peak/Compaction': df['value'].where('SO#7018' == df['code'])})
    return new_df


# In[17]:


def process_file2(input_file):
    pattern_str2 = '([0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9]*).*(SO#7001)\[(.*)].*'
    pattern2 = re.compile(pattern_str2)
    pattern3 = "[0-9]{8}"
    pattern3_str3 = re.compile(pattern3)
    m = pattern3_str3.search(input_file)
    global date_str
    if m:
        date_str = m.group(0)
    all_data2 = []
    with open(input_file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            m2 = pattern2.match(line)
            if m2 is not None:
                all_data2.append(process_line2(m2))
    df2 = pd.DataFrame(all_data2, columns=['time', 'code', 'sensor', 'values'])
    new_df2 = pd.DataFrame({'time': df2['time'], 'code': df2['code'], 'sensor': df2['sensor']})
    vals = pd.DataFrame.from_records(df2['values'].values)
    new_df2 = new_df2.join(vals)
    return new_df2


# def plot_columns(df, columns, ax=None):
#     for col in columns:
#         x = get_df(col, df)
#         if x[col].isnull().all():
#             continue
#         if ax is None:
#             ax = x.plot()
#             ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#
#         else:
#             x.plot(ax=ax)
#             ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def plot_columns(df, col_style_dict, ax=None):
    for col, style in col_style_dict.iteritems():
        x = get_df(col, df)
        if x[col].isnull().all():
            continue
        ax = x.plot(ax=ax, style=style, markersize=3.2)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return ax

# In[25]:


total_df = pd.DataFrame()
total_df2 = pd.DataFrame()
for f in ('main_20171102.log', 'main_20171103.log', 'main_20171104.log', 'main_20171105.log',
          'main_20171106.log', 'main_20171107.log', 'main_20171108.log', 'main_20171109.log',
          'main_20171110.log', 'main_20171111.log', 'main_20171112.log', 'main_20171113.log',
          'main_20171114.log', 'main_20171115.log', 'main_20171116.log', 'main_20171117.log',
          'main_20171118.log', 'main_20171119.log', 'main_20171120.log', 'main_20171121.log',
          'main_20171122.log'):
        total_df = total_df.append(process_file(f))
        total_df2 = total_df2.append(process_file2(f))


# In[26]:


print total_df
print total_df2
print total_df.describe()
print total_df2.describe()
# total_df.to_csv('DRV-100LOG00000001(1).csv')
# total_df2.to_csv('DRV-100LOG00000001.csv')


# In[27]:

plot_columns(total_df,
             {'Infeed shutter open': 'o-',
              'Infeed shutter close': 'o-',
              'Infeed shutter close. delay mode': 'o-'})
plot_columns(total_df,
             {'Compactor shutter open': 'o-',
              'Compactor shutter close': 'o-',
              'Compactor move delay': 'o-'})
plot_columns(total_df,
             {'Bottle weight': 'o-'})
plot_columns(total_df, {'Cleaning time.': 'o-'})
plot_columns(total_df, {'Weight peak/Reset': 'o-'})
plot_columns(total_df, {'Weight peak/Compaction': 'o-'})
for x in labels[1:21]:
    plot_columns(total_df2, {x: 'o-'}, plot_columns(total_df2, {x: None}))
plot_columns(total_df2, {'WT': 'o-'})

plt.show()

