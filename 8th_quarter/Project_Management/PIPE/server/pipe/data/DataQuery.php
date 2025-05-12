<?php
namespace pipe;

require_once __DIR__.'/PIPE.php';
require_once __DIR__.'/Data.php';

class DataQuery {

  // Data Table Object
  /** @var object */
  private $_builder;

  /** @var ?object */
  private $_query;

  /** @var ?array */
  private $_data;

  /** @var string */
  private $_clazz;

  /**
   * Creates a DataQuery object with a table.
   */
  function __construct($data, string $clazz) {
    $this->_builder = $data;
    $this->_query = null;
    $this->_data = null;
    $this->_clazz = $clazz;
  }

  /**
   * Orders the data
   */
  function order(array $orders) {
    $this->_builder->orderBy($orders);
    return $this;
  }

  function where(array $conditions) {
    $this->_builder->where($conditions);
    return $this;
  }

  function query($force = false) {
    if($this->_query == null || $force)
      $this->_query = $this->_builder->getQuery();
    return $this;
  }

  // Query
  function exists():bool {
    $this->query();
    return $this->_query->exists();
  }

  // Query
  function fetch($force = false) {
    $this->query($force);
    if($this->_data == null || $force)
      $this->_data = $this->_query->fetch();
    return $this;
  }

  /**
   * Deletes all the data.
   * Needs Query
   */
  function delete() : bool {
    $this->query();
    return $this->_query->delete();
  }

  /**
   * Gets one variable from the result.
   * Needs Fetch
   */
  function get(string $vname) {
    $this->fetch();
    $results = [];
    foreach($this->_data as $d) {
      $results[] = $d[$vname] ?? null;
    }
    return count($this->_data) == 1 ? $results[0] : $results;
  }

  /**
   * Counts the amount of objects in query.
   */
  function count() {
    $this->fetch();
    return count($this->_data);
  }

  /**
   * Updates the data of the objects selected.
   */
  function update(array $update):bool {
    $this->query();
    return $this->_query->update($update);
  }

  /**
   * Cross-references an index.
   * Acceptable functions:
   * CONTAINS, REMOVE, ADD
   */
  function index(string $index) {}

  /**
   * Cross-references a fragment.
   * Can only load after this.
   */
  function fragment(string $fragment) {}

  /**
   * Loads the objects of the result.
   * If n == 1, then the result is an object/null
   * An array otherwise.
   */
  function load() {
    $this->fetch();
    require_once __DIR__.'/Objects.php';
    $objs = Objects::createAll($this->_clazz, $this->_data);
    return count($objs) == 1 ? $objs[0] : $objs;
  }

};
