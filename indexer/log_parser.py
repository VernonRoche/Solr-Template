import collections
import json
from datetime import date
from pathlib import Path

keep_phrases = ["defType", ]
break_symbols = ['&', '=', '~', '*', '+']


# log_file = "/home/gerbeaud_admin/Desktop/solr/server/logs/solr.log"


def initialize_weekly_document():
    today = date.today().strftime("%d/%m/%Y")
    current_date = today.replace('/', '_')
    filename = '/home/gerbeaud_admin/Desktop/solr/server/top_searches/top_searches_' + current_date + "_WEEK_" + \
               current_date.split('_')[1] + '.json'
    Path(filename).touch()
    return filename


def get_log_lines(infile):
    query_lines = []
    with open(infile, "r") as f:
        for line in f:
            for phrase in keep_phrases:
                if phrase in line:
                    query_lines.append(line)
                    break
    return query_lines


def update_top_searches(new_data, outfile):
    with open(outfile, "w+") as f:
        sorted_data = sorted(new_data, key=new_data.get, reverse=True)
        result_data = {}
        for w in sorted_data:
            result_data[w] = new_data[w]
        json.dump(result_data, f, sort_keys=False, indent=4)


def parse_log_lines(log_lines):
    log_top_searches = {}
    for line in log_lines:
        print(line)
        query_position = line.find('&q=') + 3
        print(query_position)
        query_word = ""
        while line[query_position] not in break_symbols:
            query_word += line[query_position]
            query_position += 1
        if query_word in log_top_searches.keys():
            log_top_searches[query_word] += 1
        else:
            log_top_searches[query_word] = 1
    return log_top_searches


def parse(log_file):
    json_file = initialize_weekly_document()
    top_searches = parse_log_lines(get_log_lines(log_file))
    update_top_searches(top_searches, json_file)
    return top_searches

# parse(log_file)
