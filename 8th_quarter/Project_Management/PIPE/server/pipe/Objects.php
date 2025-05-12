<?php
namespace pipe;

require_once $PIPE_DIR.'/Util.php';

class Objects {

  /**
   * Creates a default value from a type.
   */
  static function defValue(string $type, ...$args) {
    // normal
    switch($type) {
      case 'null': return null;
      case 'bool': return false;
      case 'int': return 0;
      case 'float': return 0.0;
      case 'string': return '';
      case 'array': return [];
      case 'object': return (object) [];
    }

    // class, do not catch error
    $rc = new \ReflectionClass($type);
    return $rc->newInstance(...$args);
  }

  /**
   * Creates an object, given variables.
   */
  static function create(string $clazz, array $vars = []) {
    $obj = self::defValue($clazz);
    foreach($obj as $k => $_) {
      if(!array_key_exists($k, $vars)) continue;
      $obj->{$k} = $vars[$k];
    }
    return $obj;
  }

  /**
   * Creates all objects of given class.
   */
  static function createAll(string $clazz, array $vars = [[]]) {
    $arr = [];
    foreach($vars as $v) {
      $arr[] = self::create($clazz, $v);
    }
    return $arr;
  }

  /**
   * Returns the keys of an object or array.
   */
  static function keys($obj_like): array {
    if(is_object($obj_like)) $obj_like = get_object_vars($obj_like);
    return array_keys($obj_like);
  }

  /**
   * Copies variables from an array to another array.
   * If filter_map is null, all variables are copied.
   * If filter_map is an array, it copies only the keys included.
   * If filter_map is an associative array, it will map the new
   * array using that map.
   */
  static function copy(array &$from, array &$to, ?array $filter_map = null): void {
    if($filter_map == null) $filter_map = self::keys($from);
    
    if(is_associative($filter_map)) {
      foreach($filter_map as $k => $v) {
        $to[$v] = $from[$k] ?? null;
      }
    } else {
      foreach($filter_map as $k) {
        $to[$k] = $from[$k] ?? null;
      }
    }
  }

  /**
   * Copies variables from an object to another object.
   * If filter_map is null, all variables are copied.
   * If filter_map is an array, it copies only the keys included.
   * If filter_map is an associative array, it will map the new
   * object using that map.
   */
  static function copy_obj(&$from, &$to, ?array $filter_map = null): void {
    if($filter_map == null) $filter_map = self::keys($from);
    
    if(is_associative($filter_map)) {
      foreach($filter_map as $k => $v) {
        $to->{$v} = $from->{$k} ?? null;
      }
    } else {
      foreach($filter_map as $k) {
        $to->{$k} = $from->{$k} ?? null;
      }
    }
  }

};
