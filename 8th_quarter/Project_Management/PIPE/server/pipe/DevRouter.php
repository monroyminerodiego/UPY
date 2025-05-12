<?php
/**
 * This is a debug router to be used with the
 * PHP development server.
 * 
 * The best way to add routing on the public/ folder
 * would be to set up Apache or Nginx to try $url with
 * a .php extension. To use this approach, you need to
 * prepend PIPE.php using your php.ini.
 * 
 * If at some point you'd like to add dynamic routing
 * with PHP only, take a look at the Router and
 * RouterDriver classes.
*/
//;
// Uncomment if php.ini hasn't been set up.
// require_once __DIR__.'/PIPE.php';
{
  $url = $_SERVER["REQUEST_URI"];
  $public = realpath($_SERVER["DOCUMENT_ROOT"]);
  $urlphp = realpath("$public/$url.php");

  if($urlphp === false || strncmp($urlphp, $public, strlen($public)) !== 0) {
    return false;
  } else {
    // PIPE not obtained if we intervene.
    require_once __DIR__.'/PIPE.php';
    require $urlphp;
  }
}