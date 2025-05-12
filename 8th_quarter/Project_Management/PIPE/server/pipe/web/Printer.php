<?php
namespace pipe;

/**
 * Printer for the pages.
 */
class Printer {

  public ?Form $__form;

  function __construct() {
    $this->__form = null;
  }

  /**
   * Calls upon a client template
   * @param array|object $args
   */
  function client(string $file, $__client_args = []) {
    global $CLIENT_DIR;
    $__client_args = (array) $__client_args;
    extract($__client_args, EXTR_PREFIX_ALL, '');
    unset($__client_args);
    require "$CLIENT_DIR/$file.php";
    return $this;
  }

  /**
   * Creates an element. This method accepts a lot
   * of different syntaxes.
   * @param array|string $decl The declaration
   * of the element(s).
   */
  function elm($decl) {
    // check string
    if (\is_string($decl)) {
      echo \htmlspecialchars($decl);
      return $this;
    }

    // must be array
    ensure(\is_array($decl) == true, 'Error: Input is not an array or string');

    // length
    $len = \count($decl);
    if ($len == 0) return $this;

    // check array
    if (\is_array($decl[0])) {
      foreach ($decl as $inner) $this->elm($inner);
      return $this;
    }

    // get element tag
    $tag = $decl[0];
    unset($decl[0]);

    // continue getting parameters
    $close = $decl[1] ?? true;
    unset($decl[1]);
    $inner = $decl['.'] ?? null;
    unset($decl['.']);

    // print
    echo '<', $tag;
    foreach ($decl as $k => $v) {
      echo ' ', $k;
      if ($v === null) continue;
      echo '="', htmlspecialchars($v), '"';
    }
    echo '>';
    if ($inner != null) $this->elm($inner);
    if ($close) echo '</', $tag, '>';

    // ...
    return $this;
  }

  /**
   * Creates an element, allows to call the tag
   * as a function.
   */
  function __call($name, $arguments) {
    // check if it wants to close
    if ($name == '') throw new \Exception('Error: Empty string');

    // closing tag
    if ($name[0] == '_') {
      $name = substr($name, 1);
      $name = str_replace('_', '-', $name);
      $n = $arguments[0] ?? 1;
      for ($i = 0; $i < $n; $i++) echo '</', $name, '>';
      return $this;
    }

    // print multiple elements?
    $arglen = max(count($arguments), 1);

    // print n elements
    for ($i = 0; $i < $arglen; $i++) {
      // start outputing
      echo '<', str_replace('_', '-', $name);

      // loop array
      $args = $arguments[$i] ?? [];
      if (is_string($args)) {
        // only class
        echo ' class="', htmlspecialchars($args), '"';
      } else if (is_array($args) || is_object($args)) {
        // multiple attributes
        foreach ($args as $attr => $value) {
          // array, as check conditional attributes
          if (is_array($value)) {
            // check condition
            $_c = array_shift($value) == true;

            // 'value'=>'key' form | 'key' form 
            $_kt = array_key_first($value);
            $_true = array_shift($value);
            $_kf = array_key_first($value);
            $_false = array_shift($value);

            // set attr & value
            $attr = $_c ? $_kt : $_kf;
            $value = $_c ? $_true : $_false;
          }

          // * check string argument vs integer attributes
          if (is_string($attr)) {
            echo ' ', $attr;
            if ($value == null) continue;
            echo '="', htmlspecialchars($value), '"';
          } else if ($value !== null) {
            echo ' ', $value;
          }
          // *
        }
      } else {
        $_v = \var_export($args, true);
        throw new \Exception("[Printer] Unaccepted ($_v) for element attribute <$name>");
      }

      // end attributes
      echo '>';
    }

    // end
    return $this;
  }

  // Templating
  // General

  function stylesheets(string ...$links) {
    foreach ($links as $link) {
      echo '<link rel="stylesheet" href="', $link, '">';
    }
    return $this;
  }

  /**
   * @param string|array $links
   */
  function scripts(...$links) {
    foreach ($links as $link) {
      if(is_string($link))
        echo '<script src="', $link, '"></script>';
      else if(is_array($link)) {
        echo '<script src="', array_shift($link), '"';
        foreach($link as $attr) echo " $attr";
        echo '></script>';
      } else
        throw new \RuntimeException('Illegal script syntax');
    }
    return $this;
  }

  /**
   * Prints either:
   *  1. A string as text.
   *  2. An array as an element.
   *  3. A function, which is executed.
   */
  function print($element) {
    if (is_string($element)) $this->text($element);
    else if (is_array($element)) $this->elm($element);
    else if (is_callable($element)) $this->exe($element);
    return $this;
  }

  function icon(string $def) {
    $this->i($def)->_i();
    return $this;
  }

  /**
   * @param \Traversable $transversable
   */
  function for_each($transversable, $fn, ...$args) {
    foreach ($transversable as $k => $v) $fn($this, $k, $v, ...$args);
    return $this;
  }

  function exe($fn, ...$args) {
    $fn($this, ...$args);
    return $this;
  }

  function one_of(array $array, $select, $fn, ...$args) {
    $fn($this, $select, $array[$select], ...$args);
    return $this;
  }

  function call($obj, string $m, ...$args) {
    $obj->{$m}(...$args);
    return $this;
  }

  function cond(bool $if, $element) {
    if (!$if) return $this;
    $this->print($element);
    return $this;
  }

  function text(string ...$str) {
    foreach ($str as $s) echo htmlentities($s);
    return $this;
  }

  /**
   * @param int|float $value
   */
  function number($value, $decimals = 0, $dec_suf = 1) {
    // check negative
    if ($value < 0) {
      echo '-';
      $value = -$value;
    }

    // check sufixes
    $step = 1000;
    $sufs = ['k', 'M'];
    $vsuf = '';
    foreach ($sufs as $s) {
      if ($value < $step) break;
      $value /= $step;
      $vsuf = $s;
      $decimals = max($decimals, $dec_suf);
    }

    // send
    echo number_format($value, $decimals), $vsuf;
    return $this;
  }

  function style(array $rules) {
    echo '<style>';
    foreach ($rules as $r => $def) {
      echo $r, ' {';
      foreach ($def as $k => $v) {
        echo $k, ': ', $v, ';';
      }
      echo '}';
    }
    echo '</style>';
    return $this;
  }

  function raw(string ...$str) {
    foreach ($str as $s) echo $s;
    return $this;
  }

  /**
   * @param string|string[] $lbl
   */
  function ilabel($lbl) {
    if(is_string($lbl)) $lbl = [$lbl];
    $len = count($lbl);
    if($len == 2) {
      $icon = array_shift($lbl);
      $this->icon($icon);
      $len--;
    }
    if($len == 1) {
      $text = array_shift($lbl);
      $this->text($text);
      return $this;
    }
    throw new \RuntimeException('[pipe/Printer] Printer::label() needs 1 or 2 array elements.');
  }

  // AUTOUI EXTENSION BEGIN //

  function autoui(array $data = []) {
    $comp = array_shift($data);
    if($comp === null) throw new \RuntimeException('[PIPE/Printer] Input parameter to autoui was empty.');
    $this->client(".autoui/$comp", $data);
    return $this;
  }

  // AUTOUI EXTENSION END //

  // FORM MAKER EXTENSION BEGIN (requires autoui) //

  function formBegin(string $name, string $upload) {
    $this->__form = new Form($name);
    $this->auto_form(['data-name'=>$name,'data-upload'=>$upload,'data-autoload'=>'FormUI','data-loadorder'=>'high']);
    return $this;
  }

  /**
   * @param string|string[] $label
   */
  function formField(string $name, string $type, $label, $data = null, array $rules = []) {
    $this->client(".forms/$type", [
      'form'=>$this->__form->name,
      'name'=>$name,
      'label'=>$label,
      'data'=>$data,
      'rules'=>$rules,
    ]);
    $this->__form->rules[$name] = $rules;
    return $this;
  }

  function formRules(array $rules) {
    $this
    ->form_rules(['hidden'=>'hidden'])
      ->text(jsonEncode($rules))
    ->_form_rules()
    ;
    return $this;
  }

  function formEnd() {
    $this->_auto_form();
    $this->__form->update();
    unset($this->__form);
    return $this;
  }

  // FORM MAKER EXTENSION END //

  // ...
};

$P = new Printer();