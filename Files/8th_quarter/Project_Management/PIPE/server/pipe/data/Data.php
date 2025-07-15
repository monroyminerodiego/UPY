<?php
namespace pipe;

require_once __DIR__.'/PIPE.php';
require_once __DIR__.'/DataProvider.php';

class Data {

  // Management

  public static array $idKeys = [];
  public static array $tables = [];
  public static array $tableClasses = [];
  public static array $links = [];
  public static array $fragments = [];
  public static array $indices = [];

  public static DataProvider $provider;

  /**
   * Registers a table taking a class as the parameters.
   */
  static function registerTableClass(string $name, $clazz, string $id = 'id') {
    $fields = [];
    
    $rc = new \ReflectionClass($clazz);
    $props = $rc->getProperties(\ReflectionProperty::IS_PUBLIC);
    foreach($props as $p) {
      $pname = $p->getName();
      $ptype = $p->getType();
      if($ptype == null) throw new \RuntimeException("Class registering for table $name has a property $pname with no type!");
      if(!($ptype instanceof \ReflectionNamedType)) throw new \RuntimeException("Class registering for table $name has a property $pname with various types!");
      $ptypename = $ptype->getName();
      $fields[$pname] = $ptypename;
    }

    self::registerTable($name, $fields, $id);
    self::$tableClasses[$name] = $clazz;
  }

  /**
   * Registers a table with fields.
   * The first field must be the key.
   */
  static function registerTable(string $name, array $fields, string $id = 'id') {
    self::$tables[$name] = $fields;
    self::$idKeys[$name] = $id;
    self::$provider->registerTable($name, $id, $fields);
  }

  /**
   * Registers a link from one table to another.
   * TableFrom.id <-----> TableTo.id
   * 
   * e.i.
   * User.ID <-----> UserComment.AuthorID
   */
  static function registerLink(string $tableFrom, string $tableTo, string $keyTo) {
    // From ID
    $id = self::$idKeys[$tableFrom];
    
    // Forward Link
    $link = self::$links[$tableFrom] ?? [];
    $link[$tableTo] = $keyTo;
    self::$links[$tableFrom] = $link;

    // Backward Link
    $link = self::$links[$tableTo] ?? [];
    $link[$tableFrom] = $id;
    self::$links[$tableTo] = $link;
  }

  /**
   * Registers externally managed fragments that are attached to a table.
   */
  static function registerFragment(string $table, string $name, $clazz) {
    $frags = self::$fragments[$table] ?? [];
    $frags[$name] = $clazz;
    self::$fragments[$name] = $frags;
  }

  /**
   * Registers indices that keep a bilateral count
   */
  static function registerIndices(string $tableFrom, string $name, string $tableTo) {
    $indx = self::$indices[$tableFrom] ?? [];
    $indx[$name] = self::$idKeys[$tableTo];
    self::$indices[$name] = $indx;
  }

};

// Set Data Provider to SleekDB
Data::$provider = new SleekDBProvider();
