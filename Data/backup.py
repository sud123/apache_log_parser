import re
import pandas as pd
import os
import pytz
from datetime import datetime

#   request = re.compile(r'^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4} - - .*')

request = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (.*) "(.*?)" "(.*?)"'


def parse_str(x):
    """
    Returns the string delimited by two characters.

    Example:
        `>>> parse_str('[my string]')`
        `'my string'`
    """
    return x[1:-1]

def parse_datetime(x):
    '''
    Parses datetime with timezone formatted as:
        `[day/month/year:hour:minute:second zone]`

    Example:
        `>>> parse_datetime('13/Nov/2015:11:45:42 +0000')`
        `datetime.datetime(2015, 11, 3, 11, 45, 4, tzinfo=<UTC>)`

    Due to problems parsing the timezone (`%z`) with `datetime.strptime`, the
    timezone will be obtained using the `pytz` library.
    '''
    dt = datetime.strptime(parse_str(x), "%d/%b/%Y:%H:%M:%S %z")
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))

def filter(infile):

    if not os.path.isfile(infile):
        print("File path {} does not exist. Exiting...".format(infile))
        return -1

    # data = pd.read_csv(
    #     infile,
    #     sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
    #     engine='python',
    #     na_values='-',
    #     header=None,
    #     usecols=[0, 3, 4, 5, 6, 7, 8],
    #     names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
    #     converters={'time': parse_datetime,
    #                 'request': parse_str,
    #                 'status': int,
    #                 'size': int,
    #                 'referer': parse_str,
    #                 'user_agent': parse_str})

    # print(data)

    df = pd.read_csv(infile, sep="\\t", engine='python', header=None)

    regex = '^(?P<Host>[\d.]+)(?:\s+\S+){2}\s+\[(?P<Timestamp>[\w:/\s+]+)\]\s+"(?P<Request>[^"]+)"\s+(?P<HTTPStatus>\d+)\s+(?P<Bytes>\d+)\s+(?P<Address>"[^"]+")\s+(?P<Agent>"[^"]+")\s+(?P<NA>"[^"]+")$'
    log_df = df[0].str.extract(regex, expand=True)
    log_df[['Method', 'Page', 'Protocol']] = log_df['Request'].str.split(expand=True)

    print(log_df['Page'].value_counts()[:10].sort_values(ascending=False))




    #
    # # print(df)
    #
    #
    #
    #
    #
    #
    # df2 = pd.DataFrame(columns=["Host", "Date", "Request", "Status", "NA", "NA", "Agent"])
    #
    # # i = 0
    # # j = 0
    # #
    # # with open(infile, encoding='utf-8') as f:
    # #
    # for i in range(0, df.shape[0]):
    #     if not re.match(request, df[0][i]):
    #         # j = j+1
    #         # print("Not matched")
    #         continue
    #
    #     else:
    #         # i = i+1
    #         print("Processing")
    #         df2.loc[len(df2.index)] = list(re.match(request, df[0][i]).groups())
    #
    # print(df2)
    # # print(i)
    # # print(j)


if __name__ == '__main__':

    input_dir = "Data"
    log_file = "access.log"
    filter(os.path.join(input_dir, log_file))
