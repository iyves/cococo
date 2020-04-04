"""
File: CoCoCoDriver.py
Authors: Namu

Description:
CLI wrapper for the CoCoCo API
"""


import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from requests.exceptions import HTTPError
import argparse
import json


# driver for connecting to the CoCoCo server and returning the response of GET queries
#
class CoCoCoDriver:
    connection_string = 'http://cococo.cosyco.ru/cococo-test.py' # request URL

    # initialize a new instance of this class
    def __init__(self, args):
        # initialize the command line argument parser
        self.parser = self.init_args()

        # get the parsed command line arguments
        self.args = vars(self.parser.parse_args(args))

        # get the params to send to the server
        self.params = CoCoCoDriver.get_params(self.args)

        # create an empty response
        self.response = None


    # parse command-line arguments
    # returns: <class 'argparse.ArgumentParser'> initialize the argument parser for this class
    #
    def init_args(self):
        self.parser = argparse.ArgumentParser(description="Find the significant values of an unknown element in a sequence of "
                                                     "2 or 3 words.",
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                              epilog="Website interface: cococo.cosyco.ru"
                                              )
        self.subparsers = self.parser.add_subparsers(dest="corpus",
                                                     help="the corpus to work on",
                                                     required=True
                                                     )
        self.parser_Taiga = self.subparsers.add_parser("Taiga")
        self.parser_RNC = self.subparsers.add_parser("RNC")
        self.parser_IRU = self.subparsers.add_parser("IRU")

        self.parser.add_argument("-flimit", "--form_limit",
                                 choices=range(1,101),
                                 default=10,
                                 help="limit of words",
                                 metavar="[1-100]",
                                 type=int
                                 )
        self.parser_Taiga.add_argument("-s", "--subcorpus",
                                       choices=["All", "Poetry", "Social", "Subtitles", "Magazines", "News"],
                                       default="All",
                                       help="the subcorpus to work on"
                                      )
        # add parsing for words
        for i in range(1, 4):
            self.parser.add_argument("-w{}".format(i), "--word{}".format(i),
                                     default="",
                                     help="word #{} in the sequence".format(i)
                                     )
            self.parser.add_argument("-pos{}".format(i),
                                     choices=["S", "A", "V", "ADV", "PARTCP", "GER", "SPRO", "APRO", "PR", "CONJ", "ADVPRO",
                                              "NUM", "ANUM", "PART", "INTJ", "PRAEDIC", "PARENTH", "SYM", "X"],
                                     default="",
                                     help="part of speech for word #{} in the sequence".format(i)
                                     )
            self.parser.add_argument("-f{}".format(i), "--features{}".format(i),
                                     default="",
                                     help="features for word #{} in the sequence".format(i)
                                     )

        self.parser.add_argument("-n", "--skip",
                                 choices=range(2, 4),
                                 default=2,
                                 help="the size of each n-gram",
                                 metavar="[2-3]",
                                 type=int
                                 )
        self.parser.add_argument("-flem", "--form_str",
                                 action="store_true",
                                 help="toggle main word as lemma (token by default)"
                                 )
        self.parser.add_argument("-alem", "--form_aux",
                                 action="store_true",
                                 help="toggle auxilliary word as lemma (token by default)"
                                 )
        self.parser.add_argument('-v', '--verbose',
                                 action='count',
                                 default=0
                                 )
        return self.parser


    # turn argparse command line arguments into params for a CoCoCo query
    # args: <dict> a list of all arguments
    # returns: <set> a set of parameters for a CoCoCo GET request
    #
    def get_params(args):
        params = {
            'flimit': args['form_limit'],
            'corpus': args['corpus'],
            'flem': int(args['form_str']),
            'alem': int(args['form_aux']),
            'skip': args['skip']
        }
        for i in range(1, params['skip'] + 1):
            word = 'word{}'.format(i)
            pos = 'pos{}'.format(i)
            feature = 'features{}'.format(i)

            params[word] = args[word]
            params[pos] = args[pos]
            params[feature] = args[feature]

        if args['corpus'] == "Taiga":
            params['subcorpus'] = args['subcorpus']
            
        return params
   

    # class wrapper for sending a GET request to the CoCoCo server
    # args:
    #   <string> connection string
    #   <set> a set of parameters for a CoCoCo GET request
    #   <bool> if true, displays the request url and response
    # returns: <string> server response in JSON format
    # 
    def send_query_wrapper(self, url, params, verbose=0):
        self.response = CoCoCoDriver.send_query(url, params, verbose)
        return self.response

    # send a GET request to the CoCoCo server
    # args:
    #   <string> connection string
    #   <set> a set of parameters for a CoCoCo GET request
    #   <bool> if true, displays the request url and response
    # returns: <string> server response in JSON format
    #
    def send_query(url, params, verbose=0):
        data = ""
        # send get request to the server
        try:
            r = requests.get(url=url, params=params)
            
            if verbose > 0:
                print("-"*50);
                print("request url:\n\t", "GET\t", r.url, "\n")
                print("request headers:")
                pretty_headers = json.dumps(dict(r.headers), indent=2, 
                        ensure_ascii=False).encode('utf8')
                print(pretty_headers.decode())


                if verbose > 1:
                    print("\nrequest params:")
                    pretty_params = json.dumps(params, indent=2, 
                            ensure_ascii=False).encode('utf8')
                    print(pretty_params.decode())

                print("\nresponse code:\n\t", r.status_code)
                print("-"*50, '\n');

            # if server error, raise an exception
            r.raise_for_status()
        except HTTPError as http_err:
            print('HTTP error occurred:', http_err)
            if r.status_code == 502:
                print("Word does not exist or parameters invalid, exiting...")
            exit(0)
        except Exception as err:
            print('Other error occurred:', err)
        else:
            data = r.json()
        return data 


def main(args):
    # create an instance of the CoCoCoDriver class
    cococo = CoCoCoDriver(args[1:])
    verbose = cococo.args['verbose']
    
    # send a GET request to the CoCoCo server
    data = CoCoCoDriver.send_query(cococo.connection_string, cococo.params, verbose)
    
    # depending on verbosity level, output server response
    if verbose == 2:
        pretty_data = json.dumps(data, indent=2, 
                ensure_ascii=False).encode('utf8')
        print(pretty_data.decode())
    elif verbose == 1:
        print(data)
    else:
        print(data)
    return json.dumps(data)

if __name__ == '__main__':
    main(sys.argv)
