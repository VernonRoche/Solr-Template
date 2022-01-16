<?php
/* Solr server IP */
const SOLR_SERVER_HOSTNAME = '';

/* Enable secure mode */
const SOLR_SECURE = false;

/* HTTP connection port */
const SOLR_SERVER_PORT = ((SOLR_SECURE) ? 8443 : 8983);

/* Username for Basic Authentication */
const SOLR_SERVER_USERNAME = '';

/* Password for Basic Authentication */
const SOLR_SERVER_PASSWORD = '';

/* Name of the Solr core */
const SOLR_SERVER_PATH = '';

/* Solr query response format */
const SOLR_WT = 'json';

/* Indent */
const SOLR_INDENT = 1;

/* Request Handler */
const SOLR_QT = '/select';

/* Enable spellcheck or not */
const SOLR_SPELLCHECK = 'true';

?>
