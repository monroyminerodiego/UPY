<?php
// Creates an input element.
// Which works well for most input types
// that are text based.
/**
 * @var string $_id
 * @var string $_value
 * @var string $_type
*/
//;
{
  global $P;
  $_id = $_id ?? null;
  $_value = $_value ?? '';
  $_type = $_type ?? 'text';
  $P
  ->auto_ui([[isset($_id), 'id'=>$_id],'class'=>'ui-text','data-autoload'=>'InputUI'])
    ->input(['value'=>$_value,'type'=>$_type])
  ->_auto_ui()
  ;
}