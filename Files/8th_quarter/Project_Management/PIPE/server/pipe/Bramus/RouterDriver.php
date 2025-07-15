<?php

namespace pipe;

require_once 'pipe/Util.php';
require_once 'pipe/web/Printer.php';
require_once 'pipe/Bramus/Router.php';

/**
 * Templated Router Driver based on Braumus' Router.
 * 
 * SYNTAX:
 * 'METHOD' => [
 *   'route regex'=>['target client template', ...regex name list, ...named args,],
 *   'simple-route'=>'the-file',
 *   'same-file-name',
 *   '/u-get/(^/)+/(^/)+'=>['user-get', 'userID', 'target', 'seed'=>time(), 'debug'=>$debug],
 *   '/mounted-route' => [[...]],
 *   '.../*' => 'include', Include ALL files inside this level
 * ]
 */
class RouterDriver {

  function __construct(
    public array $routes,
    public \Bramus\Router\Router $router = new \Bramus\Router\Router()
  ) {
  }

  function mirror(string $dir) {
    // TODO: Mirror recursively all the
    // public directory.
    return $this;
  }

  function run() {
    foreach ($this->routes as $method => $rdef) {
      foreach ($rdef as $key => $value) {
        $this->parseElement($method, $key, $value);
      }
    }
    $this->router->run();
    return $this;
  }

  /**
   * @param int|string $key
   * @param string|array $value
   */
  function parseElement(string $method, $key, $value) {
    if (is_array($value)) {
      // check array of arrays
      if (is_array_array($value)) {
        // mounted route form
        foreach ($value[0] as $v_k => $v_value) {
          $this->parseElement($method, $key . $v_k, $v_value);
        }
      } else {
        // regular form
        $this->parseArray($method, $key, $value);
      }
    } else if (is_int($key)) {
      // same name form
      $this->parseArray($method, $value, [$value]);
    } else if (str_ends_with($key, '/*') && str_ends_with($value, '/*')) {
      // include form
      $this->parseInclude($method, $key, $value);
    } else if (is_string($key)) {
      // simple route form
      $this->parseArray($method, $key, [$value]);
    } else {
      // unhandled
      throw new \Exception("Illegal combination of key-value pair.");
    }
  }

  /**
   * Parses the include form
   */
  function parseInclude(string $method, string $webLevel, string $level) {
    // create directory iterator
    global $CLIENT_DIR;
    $webLevel = mb_substr($webLevel, 0, -1);
    $level = mb_substr($level, 0, -1);

    // <- check dir exists
    $dir = "$CLIENT_DIR/$level";
    if (!file_exists($dir)) return;
    $di = new \DirectoryIterator($dir);

    // foreach of this
    foreach ($di as $fi) {
      // get file name
      if (!$fi->isFile()) continue;
      $ext = $fi->getExtension();
      if ($ext != 'php') continue;

      // place into router
      $file = mb_substr($fi->getBasename(), 0, -4);
      //export([$ext, $webLevel, $level, $file]);
      $this->parseArray($method, $webLevel . $file, [$level . $file]);
    }

    // ...
  }

  /**
   * Parse the key & value pair
   */
  function parseArray(string $method, string $key, array $value) {
    $target = array_shift_alt($value);
    //export($target);
    //export($value);
    $regexNames = [];
    $namedArgs = [];
    foreach ($value as $k => $v) {
      if (is_string($k)) $namedArgs[$k] = $v;
      else $regexNames[] = $v;
    }

    // check the target for @, maybe \ in the future
    if ($target != '' && $target[0] == '\\') {
      $this->parseAbsRoute($method, $key, \substr($target, 1), $regexNames, $namedArgs);
      return;
    }

    // $ for server dir
    if ($target != '' && $target[0] == '$') {
      $this->parseServerRoute($method, $key, \substr($target, 1), $regexNames, $namedArgs);
      return;
    }

    // normal route
    $this->parseRoute($method, $key, $target, $regexNames, $namedArgs);
  }

  /**
   * Parse the route of the definition
   */
  function parseAbsRoute(string $method, string $regex, string $target, array $regexNames, array $namedArgs) {
    //log('registering route:');
    //export([$method, $regex, $target, $regexNames, $namedArgs]);
    $_this = $this;
    $this->router->match(
      $method,
      $regex,
      function (...$__client_args) use ($_this, $target, $regexNames, $namedArgs) {
        // prepare the args to be used
        global $ROOT_DIR;
        $__client_args = (array) $_this->prepareArgs($__client_args, $regexNames, $namedArgs);
        extract($__client_args, EXTR_PREFIX_ALL, '');
        unset($__client_args);
        require "$ROOT_DIR/$target.php";
      }
    );
  }

  /**
   * Parse the route of the definition
   */
  function parseServerRoute(string $method, string $regex, string $target, array $regexNames, array $namedArgs) {
    //log('registering route:');
    //export([$method, $regex, $target, $regexNames, $namedArgs]);
    $_this = $this;
    $this->router->match(
      $method,
      $regex,
      function (...$__client_args) use ($_this, $target, $regexNames, $namedArgs) {
        // prepare the args to be used
        global $SERVER_DIR;
        $__client_args = (array) $_this->prepareArgs($__client_args, $regexNames, $namedArgs);
        extract($__client_args, EXTR_PREFIX_ALL, '');
        unset($__client_args);
        require "$SERVER_DIR/$target.php";
      }
    );
  }

  /**
   * Parse the route of the definition
   */
  function parseRoute(string $method, string $regex, string $target, array $regexNames, array $namedArgs) {
    //log('registering route:');
    //export([$method, $regex, $target, $regexNames, $namedArgs]);
    global $P;
    $this->router->match(
      $method,
      $regex,
      fn (...$_args) => $P->client($target, $this->prepareArgs($_args, $regexNames, $namedArgs))
    );
  }

  /**
   * r_args is the numerical indexed array
   * regexNames is the asociative array
   * namedArgs is the constant args
   */
  function prepareArgs(array $r_args, array $regexNames, array $namedArgs): array {
    ensure(count($r_args) === count($regexNames), '[TRouterDriver] Mismatch on router args and regex names!');
    foreach ($regexNames as $k => $v) {
      $namedArgs[$v] = $r_args[$k];
    }
    return $namedArgs;
  }
};
