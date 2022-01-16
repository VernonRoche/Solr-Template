<?php
echo <<<_END
<html lang="en">
    <head>
    <title>Search Form Results</title>
    <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

  <!-- Bootstrap -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

  <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
  <link href = "https://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css"
      rel = "stylesheet">
<script src = "https://code.jquery.com/jquery-1.10.2.js"></script>
<script src = "https://code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
    </head>
    <body>
_END;
require_once $_SERVER['DOCUMENT_ROOT'].'/source/PHP/sanitizer.php';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/header.html';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/search_form.html';



if (isset($_GET['search_name'])) $search_name=sanitizeString($_GET['search_name']);
else $search_name='Unknown';
echo "<p>You searched : $search_name</p>";

require_once $_SERVER['DOCUMENT_ROOT'].'/source/javascript/javascript_search_form.html';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/footer.html';

echo <<<_END
</body>
</html>
_END;



?>
