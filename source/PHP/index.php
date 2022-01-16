<?php
echo <<<_END
<html lang="en">
    <head>
    <title>Home</title>
    <meta charset="utf-8">
    </head>
    <body>
_END;
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/header.html';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/body.html';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/search_form.html';
require_once $_SERVER['DOCUMENT_ROOT'].'/source/HTML/footer.html';

echo <<<_END
    </body>
</html>
_END;

?>


