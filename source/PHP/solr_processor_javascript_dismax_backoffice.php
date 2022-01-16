<?php
require_once $_SERVER['DOCUMENT_ROOT'] . "/source/PHP/solr_bootstrap_backoffice.php";
require_once $_SERVER['DOCUMENT_ROOT'] . "/source/PHP/sanitizer.php";

/*
 * This is a collection of parameters imported from solr_bootstrap.php used for the Solr client to connect.
 */
$options = array
(
    'hostname' => SOLR_SERVER_HOSTNAME,
    'login' => SOLR_SERVER_USERNAME,
    'password' => SOLR_SERVER_PASSWORD,
    'port' => SOLR_SERVER_PORT,
    'path' => SOLR_SERVER_PATH,
    'spellcheck' => SOLR_SPELLCHECK,
    'wt' => SOLR_WT,
    'qt' => SOLR_QT,
    'indent' => SOLR_INDENT,
);

/*
 * If someone searched something, sanitize it.
 */

if (isset($_GET['search_name'])) {
    $search_name = sanitizeString(urldecode($_GET['search_name']));
} else {
    $search_name = 'Unknown';
}

if (isset($_GET['category'])){
    $category = sanitizeString(urldecode($_GET['category']));
} else {
    $category = 'A';
}

/*
 * Check if we are doing a lighter query for the autosuggest feature
 * Else just do the normal query
 */
if (isset($_GET['autosuggest'])) {
    $autosuggest = $_GET['autosuggest'];
} else {
    $autosuggest = False;
}

/*
 * Build the query phrase, with the data passed by the user input.
 * Split the received search phrase, adding 'OR' between each word.
 * In parallel, construct a similar string, adding a '*' after each word, for autocompletion in case it needs it.
 */
$tmp_search_name = explode(' ', $search_name);
$search_name_tilde = '';
$search_name = '';
$page_number = (int)$_GET['page'];
$start = ($page_number - 1) * 10;

/*
     * If search_name is a multi word then split it with OR
     * In parallel create a similar string, adding a ~ after each word in order to use fuzzy searching
     */

foreach ($tmp_search_name as $word) {
    $search_name_tilde .= $word . '~ OR ';
    $search_name .= $word . ' OR ';
}

/*
 * Initialize Solr query, boost query, row start and page number. To be used later on.
 */
$query = substr($search_name_tilde, 0, -4) . ' OR ' . substr($search_name, 0, -4);
$boost_query = '(' . $query . ')';
$category = '(' . $category . ')';
if ($autosuggest == True) {

    /*
     * Initialize a Solr client->Fetch results from query->Send results to caller
     */
    try {
        $client = new SolrClient($options);
        $solr_query = new SolrDisMaxQuery($query);
        $response_items = send_get_response($start, $solr_query, $boost_query, $client, $category);
        $autosuggest_list=[];
        foreach ($response_items['docs'] as $item){
            $autosuggest_item['title']=$item['title'];
            $autosuggest_item['meta_reference']=$item['meta_reference'];
            array_push($autosuggest_list,$autosuggest_item);
        }
        $js_response = [
            'rows' => $solr_query->getRows(),
            'document_count' => $response_items['numFound'],
            'documents' => $autosuggest_list,];
        header('Content-type: application/json');
        header('Access-Control-Allow-Origin: https://www.gerbeaud.com');

        echo json_encode($js_response);
    } catch (SolrClientException | SolrServerException | SolrIllegalArgumentException $e) {
        print "Oops we found this error: $e";
        echo '<br>';
    }
} else {
    /* NO AUTOCOMPLETE SECTION */

    /*
     * Initialize a Solr client->Fetch results from query->Send results to caller
     */

    try {
        $client = new SolrClient($options);
        $solr_query = new SolrDisMaxQuery($query);
        $response_items = send_get_response($start, $solr_query, $boost_query, $client, $category);
        /*
         * Construct JSON-like object to be sent to the caller.
         */
        $autosuggest_list=[];
        foreach ($response_items['docs'] as $item){
            $autosuggest_item['meta_reference']=$item['meta_reference'];
            array_push($autosuggest_list,$autosuggest_item);
        }
        $js_response = [
            'page' => $page_number,
            'start' => $start,
            'rows' => $solr_query->getRows(),
            'document_count' => $response_items['numFound'],
            'documents' => $autosuggest_list,
            'is_last_page' => $response_items['numFound'] <= ($page_number * $solr_query->getRows())];
        header('Content-type: application/json');
        header('Access-Control-Allow-Origin: https://www.gerbeaud.com');
        echo json_encode($js_response);
    } catch (SolrIllegalArgumentException $e) {
        print "Oops we found this error: $e";
        echo '<br>';
    }
}

/*
 * Function to initialize most query parameters before sending it to the Solr server.
 * It adds the boost queries to increase the score for certain categories and the title.
 * Sets the results to show and from where to start.
 * Sets the minimum percentage that the result must match the query, as well as distance between words present in the
 * query but separated by words in the result documents.
 * Adds phrase fields to boost results where our query as a phrase is present.
 * Adds the fields to interrogate, as well as adding a boost to some of them.
 */
function send_get_response($start, $query, $boost_query, $client, $category)
{
    $query->useEDisMaxQueryParser();
    $query
        ->addBoostQuery('category', $category, 100.0)
        ->addBoostQuery('formatted_title', $boost_query, 2.0)
        ->addBoostQuery('formatted_heading','(Diaporama)', 0.9)
        ->addBoostQuery('formatted_heading','(Livres)', 0.9)
        ->addBoostQuery('formatted_heading','(Fiche pratique)', 1.1)
        ->addBoostQuery('formatted_heading',"(Réponse d\'expert)", 1.05)
        ->addBoostQuery('formatted_heading','(Actualités jardin)', 0.9)
        ->addBoostQuery('formatted_heading','(Outils de jardin)', 0.9)
        ->addBoostQuery('formatted_heading','(Enfants)', 0.9)
        ->addBoostQuery('formatted_heading','(Apiculture)', 0.9);
    $query
        ->setStart($start)
        ->setRows(10);
    $query
        ->setMinimumMatch('80%')
        ->setPhraseSlop(2)
        ->setQueryPhraseSlop(2)
        ->setTieBreaker(0.1);
    $query
        ->addPhraseField('title', 1.5)
        ->addPhraseField('summary', 2.0)
        ->addPhraseField('html_mainpart', 0.7);
    $query
        ->addQueryField('formatted_title', 2.5)
        ->addQueryField('summary', 1.5)
        ->addQueryField('html_mainpart', 0.5)
        ->addQueryField('meta_reference')
        ->addQueryField('absolute_path')
        ->addQueryField('thumbnail')
        ->addQueryField('heading');

    $queryResponse = $client->query($query);
    /*
     * response is the query response from Solr
     * response_items is the object we return, and is a SolrObject not containing metadata from response
     * response_items['docs'] is an array of the items found in the search query
     */
    $response = $queryResponse->getResponse();
    return $response->offsetGet('response');
}


?>