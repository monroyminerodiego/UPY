<?php
namespace pipe;
require_once __DIR__.'/WebFile.php';

/**
 * A class that obtains the
 * data from a form.
 */
class FormData {

  private object $_response;
  private object $_data;

  function __construct() {
    $this->_response = (object) [];
    $this->_response->success = false;
    $this->_response->message = null;
    $this->_response->fields = [];
    $this->_data = (object) [];
  }

  function find(string $name, $def = null) {
    // check name to find $_POST
    if(array_key_exists($name, $_POST)) return $_POST[$name];
    return $this->file($name, $def);
  }

  function post(string $name, $def = null): ?string {
    // check name to find $_POST
    return $_POST[$name] ?? $def;
  }

  function file(string $fname, $def = null): ?WebFile {
    if(array_key_exists($fname, $_FILES)) return new WebFile($_FILES[$fname]);
    return $def;
  }

  /** @return ?WebFile[] */
  function file_array(string $fname, $def = null) {
    // no file array
    if(array_key_exists($fname, $_FILES)) return $def;

    // redefine file array
    $result = array();
    foreach($_FILES[$fname] as $key1 => $value1)
      foreach($value1 as $key2 => $value2)
          $result[$key2][$key1] = $value2;
    
    // okay, now create the file objects
    $arr = [];
    foreach($result as $k => $val) {
      $arr[$k] = new WebFile($val);
    }
    return $arr;
  }

  function validate(string $formName) {
    require_once __DIR__.'/FormRules.php';
    $fr = new FormRules($formName);
    $obj = (object) [];
    foreach($fr->rules as $k => $_) {
      $obj->{$k} = $this->find($k);
    }
    foreach($fr->computeAll($obj) as $k => $v) {
      $this->_data->{$k} = $v->value;

      if(!$fr->result) {
        $st = $v->result ? 'success' : 'error';
        $this->field($k, $st, $v->message);
      }
    }
    return $fr->result;
  }

  /**
   * Adds a message to the field in the response.
   */
  function field(string $name, string $status = 'normal', ?string $message = null) {
    $this->_response->fields[] = [
      'name'=>$name,
      'status'=>$status,
      'message'=>$message
    ];
  }

  /**
   * Adds a response
   */
  function response(bool $success, ?string $message = null) {
    $this->_response->success = $success;
    $this->_response->message = $message;
  }

  function send() {
    \header('Content-Type: application/json; charset=utf-8');
    echo jsonEncode($this->_response);
  }

  function debug() {
    \pipe\export([
      '$_POST'=>$_POST,
      '$_FILES'=>$_FILES,
      '$response'=>$this->_response,
      '$data'=>$this->_data
    ]);
  }

};

