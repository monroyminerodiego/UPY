<?php
require_once __DIR__.'/../../pipe/PIPE.php';

global $PIPE_DIR;
require_once "$PIPE_DIR/FormData.php";

use pipe\FormData;

/**
 * Handler for accounts
 */
class Handler {

  // WELDPOINT
  static function signup(FormData $fd) {
    if(!$fd->validate('signup')) {
      $fd->send();
      return;
    }

    $fd->field('username',message:'Okay, info received.');
    $fd->send();
  }

  // WELDPOINT
  static function login(FormData $fd) {
    $fd->debug();
  }

};
