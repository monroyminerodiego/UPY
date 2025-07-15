<?php
namespace pipe;
require_once __DIR__.'/Util.php';

class FormRules {

  public array $rules;
  public array $values;
  public bool $result;

  function __construct(string $formName) {
    global $DATA_DIR;
    $rules = jsonLoad("$DATA_DIR/.forms/$formName.json");

    $this->rules = (array) $rules;
    $this->values = [];
    $this->result = true;
  }

  function computeAll(object $vars) {
    $out = [];

    foreach($vars as $k => $v) {
      $one = (object) $this->compute( $this->rules[$k] ?? '', $v, $vars );
      $out[$k] = $one;
    }

    return $out;
  }

  function compute(array $rules, $var, object $vars) {
    // init
    $result = true;
    $message = null;

    // loop rules for one entry
    foreach($rules as $r) {
      // prepare...
      $rname = array_shift($r);
      $msg = array_pop($r);
      $fn = self::$functions[$rname];
      foreach($r as $i => $v) $msg = str_replace("$$i", $v, $msg);
      array_unshift($r, $vars);
      array_unshift($r, $var);

      // call the function
      try {
        //\pipe\export([$rname, $r]);
        $fnres = $fn(...$r);
        if(is_array($fnres)) $var = $fnres[0];
        else $result &= $fnres;
      } catch (\Exception $ex) {
        $message = $ex->getMessage();
        \pipe\log($ex);
        $result = false;
      }

      // error
      if($result) continue;
      $message = $msg;
      break;
    }

    // compute functions
    $this->result &= $result;
    return [
      'result'=>$result,
      'value'=>$var,
      'message'=>$message
    ];
  }

  public static array $functions;

};

// Functions defined for data validation
FormRules::$functions = [
  'trim' => function(string $var, object $vars) {
    return [trim($var)];
  },
  'minlen' => function($var, object $vars, int $min) {
    return mb_strlen($var) >= $min;
  },
  'maxlen' => function($var, object $vars, int $max) {
    return mb_strlen($var) <= $max;
  },
  'notnull' => function($var, object $vars) {
    return boolval($var);
  },
  'notfield' => function($var, object $vars, string $which) {
    return $var != $vars->{$which};
  },
  'eqfield' => function($var, object $vars, string $which) {
    return $var == $vars->{$which};
  },
  'notcont' => function(string $var, object $vars, string $other) {
    $one = mb_strtolower($var);
    $two = mb_strtolower($vars->{$other});
    return !str_contains($one, $two);
  },
  'contains' => function(string $var, object $vars, string $other) {
    $one = mb_strtolower($var);
    $two = mb_strtolower($vars->{$other});
    return str_contains($one, $two);
  },
  'regex' => function(string $var, object $vars, string $regex) {
    return true;
  },
  'poke' => function($var, object $vars) {
    return true;
  },

];