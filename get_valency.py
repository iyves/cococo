"""
File: get_valency.py
Authors: Namu

Description:
Send requests to the cococo server, get back the valency + rank from a search
"""


import sys
import requests
from requests.exceptions import HTTPError
from numpy import median # for printing all fval ranks above the rank median
import argparse
import json

import CoCoCoDriver as CoCoCo
import utility


# calculate rank for each fval as: Freq. (word) rank + Freq. ratio rank
# args: <dict> a feature, ex. case, gender, number
# returns nothing
#
def calc_rank(feature):
    prev_rank = 0
    prev = -1

    # sort fvals by Freq. (word)
    feature['fvals'] = sorted(feature['fvals'], key=lambda i: i['freqs'][0], reverse=True)
    for fval in feature['fvals']:
        if fval['freqs'][0] != prev:
            prev = fval['freqs'][0]
            prev_rank += 1
        # create a column for fval rank
        fval['freqs'].append(prev_rank)

    prev_rank = 0
    prev = -1
    # sort fvals by Freq. ratio
    feature['fvals'] = sorted(feature['fvals'], key=lambda i: i['freqs'][2], reverse=True)
    for fval in feature['fvals']:
        if fval['freqs'][2] != prev:
            prev = fval['freqs'][2]
            prev_rank += 1
        # finish fval rank completion calculation
        fval['freqs'][3] += prev_rank


# print one formatted fval
# args:
#   <int> number of indents for visual spacing
#   <dict> the fval to print
# returns nothing
#
def print_fval(ind, fval):
    name = fval['val']
    corp_freq = fval['freqs'][1]
    word_freq = fval['freqs'][0]
    freq_ratio = ('%.15f' % fval['freqs'][2]).rstrip('0').rstrip('.')
    rank = fval['freqs'][3]

    print(ind + '| ' + '{:<10} | {:>10} | {:>10} | {:>15} | {:>10}'
          .format(name, corp_freq, word_freq, freq_ratio, rank))


# print the fvals of a feature that are above a specified threshold
# thresh=0 Простой подход           - Первые 3 ранга в колонке Ranks
# thresh=1 Консерванитвный подход   - Freq. ratio высше медианы
# thresh=2 Либеральный подход       - Искать самую большую дистанцию между Ranks
# TODO thresh=3 Сложный подход            -
# thresh=4 Всё                      - Всё
#
# args:
#   <dict> a feature, ex. case, gender, number
#   <int> the threshold for deciding which fvals to display
# returns nothing
#
def print_feature(feature, thresh=0):
    # sort fvals by rank
    feature['fvals'] = sorted(feature['fvals'], key=lambda i: i['freqs'][3])

    # print KLD
    print(' ' * 2 + '{:<8} (KLD = {})'.format(feature['fname'], feature['kl']))

    # print header row
    ind = ' ' * 6
    print(ind + '| ' + '{:<10} | {:>10} | {:>10} | {:>15} | {:>10}'
          .format("fval", "corp freq", "word freq", "freq ratio", "rank"))

    # print results table row depending on thresh
    if thresh == 0:
        ranks = 0
        prev_rank = -1
        for fval in feature['fvals']:
            if prev_rank != fval['freqs'][3]:
                prev_rank = fval['freqs'][3]
                ranks += 1
                if ranks > 3:
                    break
            print_fval(ind, fval)

    elif thresh == 1:
        # find the median rank
        all_ranks = [i['freqs'][3] for i in feature['fvals']]
        unique_ranks = list(dict.fromkeys(all_ranks))
        med = median(unique_ranks)

        for fval in feature['fvals']:
            if fval['freqs'][3] >= med:
                break
            print_fval(ind, fval)

    elif thresh == 2:
        max_dist = 0
        prev_rank = 0
        rank = feature['fvals'][1]['freqs'][3]

        # find the rank for the max dist
        for fval in feature['fvals']:
            cur_rank = fval['freqs'][3]
            if prev_rank != cur_rank:
                rank_diff = cur_rank - prev_rank
                if rank_diff > max_dist: #TODO > or >= ?
                    max_dist = rank_diff
                    rank = cur_rank
                prev_rank = cur_rank

        for fval in feature['fvals']:
            if fval['freqs'][3] > rank:
                break
            print_fval(ind, fval)

    elif thresh == 3:
        utility.dmsg("this code has not been implemented yet")
        pass #TODO

    elif thresh == 4:
        for fval in feature['fvals']:
            print_fval(ind, fval)
    else:
        print("Invalid value for param: thresh")


def main(args):
    # parse arguments specific to this prog
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--threshold",
                        choices=range(0,5),
                        default=0,
                        help="level of strictness for printing fvals of a feature default",
                        metavar="[0-4]",
                        type=int
                        )
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0
                        )
    known_args, driver_args = parser.parse_known_args(args)
    args = vars(known_args)
    thresh = args['threshold']
    verbose = args['verbose']

    # create an instance of the CoCoCoDriver
    cococo = CoCoCo.CoCoCoDriver(driver_args[1:])
    
    # send a GET request to the CoCoCo server
    data = cococo.send_query_wrapper(cococo.connection_string, cococo.params, verbose)
    
    # print valency
    if verbose > 0:
        print("Результаты с параметрами:")
        print("get_valency args:")
        pretty_valency_params = json.dumps(dict(args), indent=2, 
                ensure_ascii=False).encode('utf8')
        print(pretty_valency_params.decode())
        
        print("\nCoCoCoDriver params:")
        pretty_cococo_params = json.dumps(dict(cococo.args), indent=2, 
                ensure_ascii=False).encode('utf8')
        print(pretty_cococo_params.decode())
        
        if verbose == 2:    
            print("\n", data)
        if verbose > 2:    
            pretty_data = json.dumps(data, indent=2, 
                    ensure_ascii=False).encode('utf8')
            print("\n", pretty_data.decode())
        print("-"*50, '\n');

    if len(data['poses']) < 1:
        print("Нашёл слово, но результатов нет")
    else:
        # select the pose with the highest KLD
        max_kln = max(data['poses'], key=lambda i: i['kln'])
        print("{} (KLD = {})".format(max_kln['posname'], max_kln['kln']))

        # sort the features list by highest KLD
        max_kln['features'] = sorted(max_kln['features'], key=lambda i: i['kl'], reverse=True)

        for feature in max_kln['features']:
            calc_rank(feature)
            print_feature(feature, thresh)


if __name__ == '__main__':
    main(sys.argv)
