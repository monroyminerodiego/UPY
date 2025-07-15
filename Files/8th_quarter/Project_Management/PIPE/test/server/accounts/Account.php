<?php
require_once __DIR__.'/../../pipe/Data.php';

global $PIPE_DIR;
global $SERVER_DIR;

/**
 * An instance of account data.
 */
class Account {

  public string $id;
  public string $username;

};

\pipe\Data::registerTableClass('accounts', Account::class);