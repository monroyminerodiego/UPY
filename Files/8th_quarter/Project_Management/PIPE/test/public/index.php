<?php

require_once 'pipe/Bramus/RouterDriver.php';

use pipe\RouterDriver;

{
  $rd = new RouterDriver([]);

  /*
   * Re-route POST forms.
  */
  //$rd->router->match('POST', '/(@.*)', function(string $path) {
  //  global $PIPE_DIR;
  //  require_once $PIPE_DIR.'/Form.php';
  //  \pipe\Form::route($path);
  //});

  $rd->router->set404(function() {
    echo '<h1>404 PAGE</h1>';
  });

  $rd->run();
}