<?php
// Creates a toggle.
/**
 * @var bool $_checked
 * @var string $_id
 * @var string[] $_labels
 * @var string $_width
*/

use pipe\Printer;

//;
{
  global $P;

  // Modes: 'bool', 'yn', custom
  $_id = $_id ?? null;
  $_labels = $_labels ?? null;
  $_width = $_width ?? '';
  $labeled = $_labels != null ? 'labeled' : '';

  // compute name
  $name_num = ($GLOBALS['.compform'] ?? 0) + 1;
  $GLOBALS['.compform'] = $name_num;
  $name = ".compform$name_num";

  // PRINT
  $P
  ->auto_ui(['class'=>"ui-toggle $labeled",'data-autoload'=>'InputUI'])
    ->div('form-ext-control')
      ->label('form-ext-toggle__label')
        ->div('form-ext-toggle')
          ->input([
            [isset($_id), 'id'=>$_id],
            'name'=>$name,
            'type'=>'checkbox',
            'class'=>'form-ext-input',
            [$_checked??false,'checked']
          ])
          ->div(['class'=>'form-ext-toggle__toggler', [$_width != '' && $_labels, 'style'=>"width:$_width;"] ])
            ->i()->_i()
            ->cond($_labels != null, fn(Printer $P) => $P
              ->span('true')->text($_labels[0])->_span()
              ->span('false')->text($_labels[1])->_span()
            )
          ->_div()
        ->_div()
      ->_label()
    ->_div()
  ->_auto_ui()
  ;
}