<?php
namespace pipe;

use ArrayAccess;
use Countable;

require_once $PIPE_DIR.'/Util.php';

/**
 * A wrapper around PIPE's JSON functions.
 */
class JSON implements ArrayAccess, Countable {

  private $handle;
  private string $file;

  function __construct(string $file, bool $load = true, $data = null) {
    $this->file = $file;

    if($load) $this->handle = jsonLoad($file);
    else $this->handle = $data;
  }

  function __set(string $name, mixed $value): void {
    $this->handle->{$name} = $value;
  }

  function __get(string $name): mixed {
    return $this->handle->{$name} ?? null;
  }

  function __isset(string $name): bool {
    return isset($this->handle->{$name});
  }

  function __unset(string $name): void {
    unset($this->handle->{$name});
  }

  function offsetExists(mixed $offset): bool {
    return isset($this->handle[$offset]);
  }

  function offsetGet(mixed $offset): mixed {
    return $this->handle[$offset] ?? null;
  }

  function offsetSet(mixed $offset, mixed $value): void {
    $this->handle[$offset] = $value;
  }

  function offsetUnset(mixed $offset): void {
    unset($this->handle[$offset]);
  }

  function count():int {
    return count($this->handle);
  }

  function save() {
    jsonSave($this->file, $this->handle);
  }

}