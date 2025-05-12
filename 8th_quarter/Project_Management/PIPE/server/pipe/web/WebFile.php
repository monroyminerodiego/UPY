<?php
namespace pipe;

/**
 * Web file that has been uploaded.
 */
class WebFile {

  static array $errcodes = [
    0 => 'There is no error, the file uploaded with success',
    1 => 'The uploaded file exceeds the upload_max_filesize directive in php.ini',
    2 => 'The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form',
    3 => 'The uploaded file was only partially uploaded',
    4 => 'No file was uploaded',
    6 => 'Missing a temporary folder',
    7 => 'Failed to write file to disk.',
    8 => 'A PHP extension stopped the file upload.',
  ];

  public string $name = '';
  public string $type = '';
  public string $tmp_name = '';
  public int $error = 0;
  public int $size = 0;

  function __construct(array $wfile) {
    foreach($this as $k => $_) {
      $this->{$k} = $wfile[$k];
    }
  }

  function errmsg() {
    return self::$errcodes[$this->error];
  }

};
