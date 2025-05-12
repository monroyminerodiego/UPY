<?php
/**
 * @var string $_id
 * @var array $_options
 * @var string|int $_selected
 * @var string|function $_default
 */

use pipe\Printer;

//;
{
  // compute input parameters
  $_id = $_id ?? null;
  $_options = $_options ?? [];
  $_selected = $_selected ?? null;
  $_default = $_default ?? fn(Printer $P) => $P->div('--default')->raw('&nbsp;')->_div();
  $_selobj = $_options[ $_selected ] ?? $_default;

  // print HTML
  global $P;
  $P
  ->auto_ui([[isset($_id), 'id'=>$_id],'class'=>'ui-select','tabindex'=>'0','data-autoload'=>'SelectUI',[isset($_selected),'data-selected'=>"$_selected"]])
    ->div('border', 'background')
      ->div('container')
        ->div('display')->print($_selobj)->_div()
        ->div('icon opened')->icon('fas fa-caret-down')->_div()
        ->div('icon closed')->icon('fas fa-caret-left')->_div()
      ->_div()
    ->_div(2)
    ->div('dropdown', 'wrapper')
      ->for_each($_options, function(Printer $P, $k, $v) use($_selected) {
        $act = $_selected === $k ? 'active' : '';
        $P
        ->div(['class'=>"option $act",'tabindex'=>'0','data-value'=>"$k"])
          ->print($v)
        ->_div()
        ;
      })
    ->_div(2)
  ->_auto_ui()
  ;
}