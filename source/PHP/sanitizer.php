<?php
function sanitizeString($var): string
{
    $var=stripslashes($var);
    $var=strip_tags($var);
    return htmlentities($var);
}

function sanitizeMYSQL($connexion, $var): string
{
    $var=$connexion->real_escape_string($var);
    return sanitizeString($var);
}
