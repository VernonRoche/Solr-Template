import pysolr

from index_actions import *

###
#   This is the main file called by the Flask server. It gets at least 2 parameters.
#   First parameter is the action to take (initialize, wipe etc.) defined in the initialize_table dictionary.
#   The 2 to n parameters are then appended into a list for using them later.
###

initialize_table = {
    'initialize': 0,
    'wipe': 1,
    'add': 2,
    'reset_category': 3,
    'remove': 4,
}


def main(args):
    ###
    #   Initialize Solr client, decide which action is taken and parse the meta_references passed in a list.
    ###
    solr = pysolr.Solr()
    initialize = initialize_table[args[0]]
    args = args[1:]
    references = []
    for x in args:
        references.append(x)

    ###
    #   Initialize the whole index
    ###
    if initialize == 0:
        # Articles-Fiches-Reponses Experts-Livres-Diaporamas
        reference_letters = ['A', 'F', 'X', 'L', 'S']
        add_list = []
        for letter in reference_letters:
            create_index_add_list(letter, add_list)
        # Must pass a list of dictionaries to update_index
        update_index(add_list, solr)
        print("Correctly initialized the Solr index.")

    ###
    # Remove everything from index
    ###
    elif initialize == 1:
        reset_index(solr)
        print("Correctly deleted all documents from Solr index.")

    ###
    # Add the 2 to n parameters to the index
    ###
    elif initialize == 2:
        # Convert them to json
        add_list = reference_to_json(references)
        update_index(add_list, solr)
        print("Correctly deleted obsolete pages and added new documents to Solr index.")

    ###
    # Removes all pages from the category and re-indexes them
    ###
    elif initialize == 3:
        # Get the letter of the reference we passed. We will reset this category
        category = references[0][0]
        add_list = []
        create_index_add_list(category, add_list)
        # Must pass a list of dictionaries to update_index
        update_index(add_list, solr)
        print("Correctly reset the Solr index category.")

    ###
    #   Remove the 2 to n parameters from the index
    ###
    elif initialize == 4:
        # Convert the references to json
        remove_list = reference_to_json(references)
        remove_deprecate_index(remove_list, solr)
        print("Correctly removed the specified pages in the Solr index.")


main(["add","A50"])
