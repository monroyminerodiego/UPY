<?php
namespace pipe;

/**
 * Defines a data table which may be obtained from a SQL or NoSQL Database.
 */
class DataTable {

  /**
   * String ID field
   */
  public string $id;

  /**
   * The name/type definition of the fields inside.
   */
  public array $def;

  /**
   * The class which will be used to receive the data.
   */
  public $class;

  /**
   * Constructs the table based on a class.
   */
  function __construct($class, string $id = 'id') {
    $this->class = $class;
    $this->id = $id;
    
    // Check definition is compatible
    $obj = new \ReflectionClass($class);
    $props = $obj->getProperties(\ReflectionProperty::IS_PUBLIC);
    
    // Save to definition
    $this->def = [];
    foreach($props as $p) {
      $this->def[$p->getName()] = (string) $p->getType();
    }
  }

};
