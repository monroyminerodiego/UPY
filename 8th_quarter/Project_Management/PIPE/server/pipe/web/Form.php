<?php
namespace pipe;
require_once __DIR__.'/PIPE.php';
require_once __DIR__.'/Util.php';
require_once __DIR__.'/FormRules.php';
require_once __DIR__.'/FormData.php';

/**
 * Form Maker Class
 */
class Form {

  public string $name;
  public array $rules;

  function __construct(string $name) {
    $this->name = $name;
    $this->rules = [];
  }

  function validate(object $data) {
    $fr = new FormRules($this->rules);
    return $fr->computeAll($data);
  }

  function update() {
    // check if file exists
    global $DATA_DIR;
    $dir = "$DATA_DIR/.forms/$this->name.json";
    if(file_exists($dir)) return $this;

    // write to the file.
    $this->save();
    return $this;
  }

  function save() {
    global $DATA_DIR;
    $dir = "$DATA_DIR/.forms/$this->name.json";
    jsonSave($dir, $this->rules);
    return $this;
  }

  function load() {
    global $DATA_DIR;
    $dir = "$DATA_DIR/.forms/$this->name.json";
    $this->rules = jsonLoad($dir);
    return $this;
  }

  /**
   * Routes to the callback.
   * Syntax: @path/to/file::function
   */
  static function route(string $path) {
    // check starts with @
    if(!str_starts_with($path, '@')) throw new \Exception("[pipe/FormMaker] Bad syntax: {$path}");

    // Split the string by '::' to get the file and the method
    $_arr = explode('::', substr($path, 1), 2);
    if(count($_arr) != 2) throw new \Exception("[pipe/FormMaker] Bad syntax: {$path}");
    list($file, $method) = $_arr;

    // Convert file path to file system path
    global $SERVER_DIR;
    $filePath = realpath($SERVER_DIR."/$file.php");

    // Check if the file exists inside the server
    if (!str_starts_with($filePath, $SERVER_DIR)) {
      throw new \Exception("[pipe/FormMaker] File out of bounds: {$filePath}");
    }

    // Check if the file exists
    if (!file_exists($filePath)) {
      throw new \Exception("[pipe/FormMaker] File not found: {$filePath}");
    }

    // Require the file
    require_once $filePath;

    // Check if the class exists
    $className = basename($file);
    if (!class_exists($className)) {
      throw new \Exception("[pipe/FormMaker] Class not found: {$className}");
    }

    // Check if the method exists
    if (!method_exists($className, $method)) {
      throw new \Exception("[pipe/FormMaker] Method not found: {$method}");
    }

    // Check if the method accepts FormData object and returns void
    $reflectionMethod = new \ReflectionMethod($className, $method);
    if ($reflectionMethod->hasReturnType() && $reflectionMethod->getReturnType()->getName() !== 'void') {
      throw new \Exception("[pipe/FormMaker] Method {$method} in {$className} must have a return type of void.");
    }

    // get parameters
    $parameters = $reflectionMethod->getParameters();
    if (count($parameters) != 1 || $parameters[0]->getType()->getName() !== 'pipe\FormData') {
      throw new \Exception("[pipe/FormMaker] Method {$method} in {$className} must accept an object of type \\pipe\\FormData");
    }

    // Call the method with try-catch block
    try {
      $reflectionMethod->invoke(null, new FormData());
    } catch (\Exception $e) {
      throw new \Exception("[pipe/FormMaker] Error calling {$method} in {$className}: " . $e->getMessage(), 0, $e);
    }
  }

};
