<?php
namespace pipe;

require_once __DIR__.'/PIPE.php';
require_once __DIR__.'/DataQuery.php';
require_once __DIR__.'/SleekDB/Store.php';

/**
 * Represents a Provider that can save and
 * load data.
 */
abstract class DataProvider {

  abstract function getName();

  abstract function getTable(string $name);

  abstract function registerTable(string $table, string $id, array $fields);

  /**
   * Fetches data from a table with some conditions.
   * @return \DataQuery
   */
  abstract function query(string $table);

  /**
   * Inserts a data object into the table.
   */
  abstract function insert(string $table, $data);

};

/**
 * Uses SleekDB as DataProvider.
 */
class SleekDBProvider extends DataProvider {

  private array $tables = [];
  private array $indx = [];

  function __construct() {}

  function getName() {
    return 'SleekDB';
  }

  function registerTable(string $table, string $id, array $fields) {
    global $DATA_DIR;
    $this->tables[$table] = new \SleekDB\Store($table, $DATA_DIR, [
      "timeout" => false,
      "primary_key" => $id,
    ]);
  }

  function getTable(string $table) {
    return $this->tables[$table] ?? null;
  }

  function registerIndex() {}

  function getIndex() {}

  function query(string $table) {
    $tobj = $this->getTable($table);
    if($tobj == null) throw new \Exception("Table '$table' does not exist.");
    return new DataQuery($tobj, Data::$tableClasses[$table] ?? 'object');
  }

  function insert(string $table, $data) {}

};
