import pandas as pd
import os
import argparse


def most_requested(df, col, n):

    # print(df[col].value_counts()[:n].sort_values(ascending=False))
    # print(df[col].value_counts()[df[col].value_counts() == df[col].value_counts().max()])
    # print(df[col].value_counts().keys()[:n])
    return df[col].value_counts()[:n]


def top_ten_requests(log_df):

    # print(log_df['Page'].value_counts()[:10].sort_values(ascending=False))
    top10_successful = most_requested(log_df, 'Page', 10)
    print("Top 10 Successful Requests:")
    print(top10_successful)
    print("")


def percent_successful(log_df):

    log_df['HTTPStatus'] = pd.to_numeric(log_df['HTTPStatus'], errors='coerce')
    log_df2 = log_df.copy()
    log_df2 = log_df2.apply(lambda x: True
                        if x['HTTPStatus'] >= 200 and x['HTTPStatus'] < 400 else False, axis=1)

    num_rows = len(log_df2[log_df2 == True].index)
    percent_successful = num_rows/len(log_df.index)*100
    print("Percentage of Successful requests: " + str(percent_successful) + "%")
    print("")


def percent_unsuccessful(log_df):

    log_df['HTTPStatus'] = pd.to_numeric(log_df['HTTPStatus'], errors='coerce')
    log_df2 = log_df.copy()
    log_df2 = log_df2.apply(lambda x: True
                        if x['HTTPStatus'] >= 200 and x['HTTPStatus'] < 400 else False, axis=1)
    num_rows = len(log_df2[log_df2 == True].index)
    percent_unsuccessful = (len(log_df.index) - num_rows) / len(log_df.index) * 100
    print("Percentage of Unsuccessful requests: " + str(percent_unsuccessful) + "%")
    print("")


def top_ten_unsuccessful_pages(log_df):

    log_df['HTTPStatus'] = pd.to_numeric(log_df['HTTPStatus'], errors='coerce')
    log_df2 = log_df.copy()
    log_df2 = log_df2.apply(lambda x: True
                        if x['HTTPStatus'] >= 200 and x['HTTPStatus'] < 400 else False, axis=1)
    top10_unsuccessful = most_requested(log_df[log_df2 == False], 'Page', 10)
    print("Top 10 Unsuccessful Requests:")
    print(top10_unsuccessful)
    print("")


def top_ten_hosts(log_df):

    top10_hosts = most_requested(log_df, 'Host', 10)
    print("Top 10 Hosts:")
    print(top10_hosts)
    print("")


def top_ten_hosts_pages(log_df):

    top10_hosts = most_requested(log_df, 'Host', 10)
    print("Top 10 Hosts:")
    print(top10_hosts)
    print("")

    list_top10_host = top10_hosts.index.tolist()

    for host in list_top10_host:
        print("Top 5 Requests for Host: " + str(host))
        top_5_pages = most_requested(log_df[log_df['Host'] == host], 'Page', 5)
        print(top_5_pages)
        print("")


def log_parser(infile):

    if not os.path.isfile(infile):
        print("File path {} does not exist. Exiting...".format(infile))
        return -1

    df = pd.read_csv(infile, sep="\\t", engine='python', header=None)

    regex = '^(?P<Host>[\d.]+)(?:\s+\S+){2}\s+\[(?P<Timestamp>[\w:/\s+]+)\]\s+"(?P<Request>[^"]+)"\s+(?P<HTTPStatus>\d+)\s+(?P<Bytes>\d+)\s+(?P<Address>"[^"]+")\s+(?P<Agent>"[^"]+")\s+(?P<NA>"[^"]+")$'
    log_df = df[0].str.extract(regex, expand=True)
    log_df[['Method', 'Page', 'Protocol']] = log_df['Request'].str.split(expand=True)

    return log_df

    # # print(log_df['Page'].value_counts()[:10].sort_values(ascending=False))
    # top10_successful = most_requested(log_df, 'Page', 10)
    # print("Top 10 Successful Requests:")
    # print(top10_successful)
    # print("")
    #
    # log_df['HTTPStatus'] = pd.to_numeric(log_df['HTTPStatus'], errors='coerce')
    # log_df2 = log_df.copy()
    # log_df2 = log_df2.apply(lambda x: True
    #                     if x['HTTPStatus'] >= 200 and x['HTTPStatus'] < 400 else False, axis=1)

    # num_rows = len(log_df2[log_df2 == True].index)
    # percent_successful = num_rows/len(log_df.index)*100
    # print("Percentage of Successful requests: " + str(percent_successful) + "%")
    # print("")
    #
    # percent_unsuccessful = (len(log_df.index)-num_rows)/len(log_df.index)*100
    # print("Percentage of Unsuccessful requests: " + str(percent_unsuccessful) + "%")
    # print("")

    # top10_unsuccessful = most_requested(log_df[log_df2 == False], 'Page', 10)
    # print("Top 10 Unsuccessful Requests:")
    # print(top10_unsuccessful)
    # print("")

    # top10_hosts = most_requested(log_df, 'Host', 10)
    # print("Top 10 Hosts:")
    # print(top10_hosts)
    # print("")
    #
    # list_top10_host = top10_hosts.index.tolist()
    # # log_df3 = log_df.copy()
    # # log_df3 = log_df3.apply(lambda x: True
    # #             if x['Host'] in list_top10_host else False, axis=1)
    # # # print(log_df[log_df3 == True])
    #
    # for host in list_top10_host:
    #     print("Top 5 Requests for Host: " + str(host))
    #     top_5_pages = most_requested(log_df[log_df['Host'] == host], 'Page', 5)
    #     print(top_5_pages)
    #     print("")


def add_args(parser):

    parser.add_argument('-f', '--log_file', metavar='LOG_FILE', type=argparse.FileType('r'),
                        help='Path to the Apache access log file')
    parser.add_argument('-tp', '--top_ten_pages', action='store_true', help='Top 10 Requested Pages')
    parser.add_argument('-ps', '--percent_successful', action='store_true', help='Percentage of successful requests')
    parser.add_argument('-pu', '--percent_unsuccessful', action='store_true', help='Percentage of unsuccessful requests')
    parser.add_argument('-tu', '--top_ten_unsuccessful_pages', action='store_true', help='Top 10 unsuccessful page requests')
    parser.add_argument('-th', '--top_ten_hosts', action='store_true', help='The top 10 hosts making the most requests, displaying the IP address and number of requests made.')
    parser.add_argument('-thp', '--top_ten_hosts_pages', action='store_true', help='For each of the top 10 hosts, shows the top 5 pages requested and the number of requests for each.')

    return parser


if __name__ == '__main__':

    input_dir = "Data"
    log_file = "access.log"

    parser = argparse.ArgumentParser(description='An Apache access log parser')
    parser = add_args(parser)
    args = parser.parse_args()

    if args.log_file:
        log_df = log_parser(args.log_file)
    else:
        log_df = log_parser(os.path.join(input_dir, log_file))

    if args.top_ten_pages:
        top_ten_requests(log_df)

    if args.percent_successful:
        percent_successful(log_df)

    if args.percent_unsuccessful:
        percent_unsuccessful(log_df)

    if args.top_ten_unsuccessful_pages:
        top_ten_unsuccessful_pages(log_df)

    if args.top_ten_hosts:
        top_ten_hosts(log_df)

    if args.top_ten_hosts_pages:
        top_ten_hosts_pages(log_df)