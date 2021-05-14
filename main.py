# section imports
from datetime import datetime
import bar_chart_race as bcr
import pandas as pd
import requests
import csv

# section parameters
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
name_for_download = 'Covid-data.csv'
name_of_prepered = 'Prepered_data.csv'
response = requests.get(url)
countries = ['Date', 'Poland', 'Russia', 'Germany', 'United States']


# section functions
def download_file(url):
    '''

    :param url: url to download_file
    :return:
    '''
    response = requests.get(url)
    output = open(name_for_download, 'wb')
    output.write(response.content)
    output.close()


def read_file(name_for_download):
    '''

    :param name_for_download: name of a file to open
    :return: dataframe from the file
    '''
    data = pd.read_csv(name_for_download)
    return data


def extract_data(data):
    '''

    :param data: dataframe from downloaded file
    :return: tables of dates and total cases extracted from file
    '''
    dates = list(set(data['date'].to_list()))
    dates.sort()
    total_cases = []
    for country in countries:
        total_cases_per_country = []
        for date in dates:
            get_data = data.loc[(data['location'] == country) & (data['date'] == date)]
            total_cases_per_country.append(get_data['total_cases'].to_list())
        total_cases.append(total_cases_per_country)
    return dates, total_cases


def create_prepared_file(dates, total_cases, file_name):
    '''

    :param dates: dates from downoladed file
    :param total_cases: total cases in specified country from downoladed file
    :param file_name: name of downloaded file
    :return: void
    '''
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(countries)
        i = 0
        for date in dates:
            data_to_write = [datetime.strptime(date, '%Y-%m-%d').date()]
            float_to_add = 0
            for j in range(1, 5):
                try:
                    float_to_add = float(''.join(total_cases[j][i]))
                    data_to_write.append(float_to_add)
                except ValueError:
                    data_to_write.append(0.0)
                except TypeError:
                    data_to_write.append(total_cases[j][i][0])
            writer.writerow(data_to_write)
            i += 1


def generate_bar_chart(name_of_prepered):
    '''

    :param name_of_prepered: Name of the file prepered to generate bar chart race
    :return: 
    '''
    data_for_visualisation = pd.read_csv(name_of_prepered)
    data_for_visualisation = data_for_visualisation.set_index('Date')
    bcr.bar_chart_race(df=data_for_visualisation, orientation='h',
                       filename='COVID.mp4',
                       sort='desc',
                       n_bars=6,
                       fixed_order=False,
                       fixed_max=True,
                       steps_per_period=30,
                       interpolate_period=False,
                       label_bars=True,
                       bar_size=.95,
                       period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
                       period_fmt=('Date - {x}'),
                       period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                                         's': f'Total cases: {v.nlargest(6).sum():,.0f}',
                                                         'ha': 'right', 'size': 8, 'family': 'Courier New'},
                       perpendicular_bar_func='median',
                       period_length=100,
                       figsize=(5, 3),
                       dpi=144,
                       cmap='dark12',
                       title='COVID-19 Cases by Country',
                       title_size='',
                       bar_label_size=7,
                       tick_label_size=7,
                       shared_fontdict={'family': 'Helvetica', 'color': '.1'},
                       scale='linear',
                       writer=None,
                       fig=None,
                       bar_kwargs={'alpha': .7},
                       filter_column_colors=False)


# section main
if __name__ == '__main__':
    download_file(url)
    data = read_file(name_for_download)
    dates, total_cases = extract_data(data)
    create_prepared_file(dates, total_cases, name_of_prepered)
    generate_bar_chart(name_of_prepered)
