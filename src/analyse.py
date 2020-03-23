"""
Set the following three parameters.
Plotting will run subsequently.

scale: int, scales daily data. 7: one week. 30: one month. 0.5: half day.
no_periods: int, determine scaled-day periods.
measures: list, takes the desired measures from header_dict.
header_dict: dict, output from load_data.ipynb.
files: list, output from load_data.ipynb.
"""
import matplotlib.dates as mdates
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from load_data import load_data

# Init variables
df, files, header_dict = load_data()
scale = 7 # 1 = single day, 7 = week, etc.
no_periods = 52 # numer of periods, ie 10 weeks; scale =7, no periods = 10
measures = ['no2','no','pm10'] 

def fix_series(series, missing, flag):
    """ Calls a series recursively and patches the minimal datetime value with the pervious one
        continues with the maxium. Et cetera.
        Not error proof, ie whole series == missing will recurse to the limit.
        Make sure to not pass an empty series.
    """
    if len(missing) == 0: return series
    if flag == 'min':
        if missing.min() < series['datetime'].min(): 
            pass
        else:
            insert = series.loc[series['datetime'] == missing.min() - timedelta(minutes=30),:].copy()
            datetime = insert.loc[:,'datetime']
            insert.loc[:,'datetime'] = datetime+timedelta(minutes=30)
            series = series.append(insert)
            missing = missing[missing != missing.min()]
            return fix_series(series, missing, 'max')
    if flag == 'max':
        if missing.max() > series['datetime'].max(): 
            pass
        else:
            insert = series.loc[series['datetime'] == missing.max() + timedelta(minutes=30),:].copy()
            datetime = insert.loc[:,'datetime']
            insert.loc[:,'datetime'] = datetime-timedelta(minutes=30)
            series = series.append(insert)
            missing = missing[missing != missing.max()]
            return fix_series(series, missing, 'min')
        
null_sum = df.isnull().sum(axis=0)
cols = null_sum[null_sum == 0].index.tolist()

period = 2*24*scale # day*scale

last_date = df['datetime'][len(df)-1]
start_date = last_date - timedelta(days=no_periods*scale)
days = (last_date-start_date).days
days /= scale 

idx = pd.date_range(start_date, last_date, freq='30min')[1:]
_ = df.loc[df['datetime'].isin(idx),]

""" This snippet takes care that missing records (hopefully few) mess with our plotting.
    We use fix_series() - the left-most missing value gets its left neighbor. The right-most missing value its right neighbor.
"""
print("INPUT - Location, timestamps covered (%): ",[round((len(_.loc[i])/(period*no_periods)) * 100,2) for i in files])
for i in files:
    if len(_.loc[i]) != period*no_periods:
        series = _.loc[i]
        missing = idx[~idx.isin(series['datetime'])]
        series = fix_series(series,missing,'min')
        series.sort_values('datetime', inplace=True)
        _ = _.loc[~(_.index == i)].append(series)
print('OUTPUT - Location, timestamps covered (%): "',[round((len(_.loc[i])/(period*no_periods)) * 100,2) for i in files])

def plotit(files,measures,days,header_dict,period):
    """
    Squished into a function for importing. For later refactoring.
    """
    colmap = cm.get_cmap('twilight_shifted', int(days))

    no_meas = len(measures) #measures
    no_locs = len(files) #locations

    fig, ax = plt.subplots(nrows=no_meas,ncols=3,squeeze=False)
    fig.set_size_inches(8.5*no_locs, 5.*no_meas)

    for d in range(int(days)): # cuts timeframe
        for i in range(no_locs): # selects location
            for j in range(no_meas): # selects measure
                measure = measures[j]
                title = list(header_dict.keys())[list(header_dict.values()).index(measure)]
                t = [i/2 for i in range(period)] # Half hour intervals, whole day
                s = np.log(_.loc[_.index == files[i],measure][d*period:(d+1)*period]+1)

                if d==days-1:
                    ax[j,i].plot(t,s,'r-', linewidth=2) #draw last line red
                else:
                    ax[j,i].plot(t,s,'r-',alpha=(d/days),c=colmap(days-d))
                ax[j,i].set(xlabel='Hour', ylabel=title+' Concentration. (log)',
                   title=files[i])
                ax[j,i].grid()
                ax[j,i].format_xdata = mdates.DateFormatter('%d-%H')


    fig.savefig("../output.png")
    plt.show()

plotit(files,measures,days,header_dict,period)