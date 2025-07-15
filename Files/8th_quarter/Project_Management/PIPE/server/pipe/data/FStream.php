<?php
namespace pipe;

require_once $PIPE_DIR.'/Util.php';

/**
 * A robust objectified implementation of PHP's
 * file operations.
 */
class FStream {

  private $handle;
  private string $file;

  public bool $bad;
  public int $count;

  function __construct(string $file, string $mode) {
    $this->file = $file;
    $this->handle = fopen($file, $mode);
    $this->count = 0;
    $this->bad = false;
  }

  function __destruct() {
    if($this->handle != null) $this->close();
  }

  function seek(int $offset, int $mode = SEEK_SET) {
    $r = fseek($this->handle, $offset, $mode);
    if($r != 0) $this->bad = true;
  }

  function tell() {
    $r = ftell($this->handle);
    if($r === false) {
      $this->bad = true;
      return -1;
    }
    return $r;
  }

  function size() {
    $i = $this->tell();
    if($this->bad) return 0;

    $this->seek(0, SEEK_END);
    if($this->bad) return 0;

    $size = $this->tell();
    if($this->bad) return 0;

    $this->seek($i, SEEK_SET);
    if($this->bad) return 0;

    return $size;
  }

  function read(int $length) {
    $d = fread($this->handle, $length);

    if($d === false) {
      $this->count = 0;
      $this->bad = true;
      return '';
    }

    $this->count = strlen($d);
    return $d;
  }

  function write(string $data) {
    $n = fwrite($this->handle, $data);
    if($n === false) {
      $this->bad = true;
      $this->count = 0;
      return;
    }
    $this->count = $n;
  }

  function eof() {
    return feof($this->handle);
  }

  function close() {
    $r = fclose($this->handle);
    if(!$r) {
      log("[pipe/FStream] WARN: Could not properly close handle of file '$this->file'.");
    }
    $this->handle = null;
    return $r;
  }

  function delete() {
    $this->close();
    $r = unlink($this->file);
    if(!$r) {
      log("[pipe/FStream] WARN: Could not properly delete file '$this->file'.");
    }
    return $r;
  }

}
