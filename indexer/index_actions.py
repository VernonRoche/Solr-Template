import time

from bs4 import BeautifulSoup

from json_request import *


###
#   Takes the title and removes all small words which might polute it.
#   This is used to populate the formatted_title field of a Solr item.
###
def remove_articles_title(title_string):
    article_list = [' le ', ' la ', ' les ', ' me ', ' mes ', ' ma ', ' tu ', ' te ', ' ta ', ' ton ', ' que ', ' ne ',
                    ' se ', 'ce ', ' ses ', ' ces ', ' au ', ' vos ', ' et ', ' en ', ' pas ', ' pour ', ' y ',
                    ' je ', ' de ', ' des ', ' du ', ' ou ', ' à ', ' un ', ' une ', ' lesquels ', ' lesquelles ',
                    ' quel ', ' quelle ', ' lequel ', ' faut-il ', ' quels ', ' quelles ', ' aux ', ' bien ']
    article_list_apostrophe = ['l’', 'm’', 'qu’', 'n’', 's’', 'j’', 't’', 'd’']
    title_string = ' ' + title_string.lower()
    for article in article_list_apostrophe:
        title_string = title_string.replace(article, '')
    for article in article_list:
        title_string = title_string.replace(article, ' ')
    return title_string


###
#   If a page from new_data is present in the Solr index, remove it
###
def remove_deprecate_index(new_data, solr_client):
    to_delete = []
    for data in new_data:
        # Search if the meta_reference exists in the index
        if len(solr_client.search('meta_reference:' + data['meta_reference'])) != 0:
            to_delete.append(data['meta_reference'])
    for x in to_delete:
        solr_client.delete(q='meta_reference:' + x)


###
#   Removes older versions of pages we want to add then adds everything to the index
###
def update_index(new_data, solr_client):
    remove_deprecate_index(new_data, solr_client)
    # After deletion of old pages, add everything in the index
    solr_client.add(new_data)


###
#   Removes everything from the index
###
def reset_index(solr_client):
    solr_client.delete(q='*:*')


###
#   For a specified page category, get it's lowest and highest page numbers.
#   Convert all references present in the category to json format.
#   Parse contents from each json and add them to the list passed as a parameter.
###
def create_index_add_list(category_letter, add_list):
    bound = get_category_bound(category_letter)
    for i in range(0, (bound[1] - bound[0])):
        time.sleep(0.1)
        response = get_json_from_url(category_letter + str(bound[0] + i))
        append_beautified_json_to_list(add_list, response)


###
#   Parses a json/dictionary and adds it to the list passed as a parameter
###
def append_beautified_json_to_list(add_list, response):
    if response is not None:
        response['category'] = response['meta_reference'][0]
        if response['title'] is None:
            response['title'] = 'Title'
        else:
            response['title'] = BeautifulSoup(response['title'], "html.parser").get_text()
            response['formatted_title'] = remove_articles_title(response['title'])
        if response['summary'] is None:
            response['summary'] = 'Summary'
        else:
            response['summary'] = BeautifulSoup(response['summary'], "html.parser").get_text()
        if response['html_mainpart'] is None:
            response['html_mainpart'] = 'Mainpart'
        else:
            response['html_mainpart'] = BeautifulSoup(response['html_mainpart'], "html.parser").get_text()
        if response['absolute_path'] is None:
            response['absolute_path'] = "Path"
        if response['thumbnail'] is None:
            response['thumbnail'] = "Thumbnail"
        if response['heading'] is None:
            response['heading'] = "Fiche_pratique"
        else:
            response['formatted_heading'] = response['heading'].replace(" ", "_")
        add_list.append(response)


###
#   Takes a list of meta_references, sends a request to gerbeaud.com and returns a list of dictionaries with
#   the data corresponding to each reference.
###
def reference_to_json(references):
    json_list = []
    for x in references:
        json_file = get_json_from_url(x)
        append_beautified_json_to_list(json_list, json_file)
    return json_list


###
#   Check if the index needs to be updated (TO BE IMPLEMENTED AND FINISHED)
###
def is_updated(solr_client):
    reference_letters = ['A', 'F', 'X', 'L', 'S']
    for letter in reference_letters:
        new_bounds = get_category_bound(letter)
        if len(solr_client.search('meta_reference:' + letter + str(new_bounds[1]))) == 0:
            return True
    return False


# test_string = {
#     "title": "<p>Something</p><h3>Something</h3>",
#     "html_mainpart": "<p>Main part</p><tag></tag>",
#     "summary": "<h2>Summary</h2>",
#     "meta_reference": "A250",
#     "absolute_path": "path",
#     "heading": "Fruits & legumes de saison",
#     "thumbnail": "",
# }
#
# test_list = []
# append_beautified_json_to_list(test_list, test_string)
# print(test_list)

# test_list = reference_to_json("A1500")
# print(test_list)
