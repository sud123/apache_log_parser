***Apache Access Log Parser***

Author: Sudarshan Kumar
Date: 21-Mar-2021

************
Description: Parses an Apache Access log and computes request statistics
************

*************
Dependencies:
    * Python 3.6 or higher

Python Libraries:
    * pandas
    * argparse
*************

*****************
Steps to Execute:

Assumption - Necessary dependencies mentioned above is installed and path to the python exec is set in the PATH env.
--------------
python apache_log_parser.py <arguments>
eg - python apache_log_parser.py -f "C:\data\access.log" -tp (Prints Top 10 Requested Pages)
--------------
Arguments:
    * '-f', '--log_file', desc='Path to the Apache access log file' (argument)
    * '-tp', '--top_ten_pages', desc='Top 10 Requested Pages' (flag)
    * '-ps', '--percent_successful', desc='Percentage of successful requests' (flag)
    * '-pu', '--percent_unsuccessful', desc='Percentage of unsuccessful requests' (flag)
    * '-tu', '--top_ten_unsuccessful_pages', desc='Top 10 unsuccessful page requests' (flag)
    * '-th', '--top_ten_hosts', desc='The top 10 hosts making the most requests, displaying the IP address and number of requests made.' (flag)
    * '-thp', '--top_ten_hosts_pages', desc='For each of the top 10 hosts, shows the top 5 pages requested and the number of requests for each.' (flag)
******************