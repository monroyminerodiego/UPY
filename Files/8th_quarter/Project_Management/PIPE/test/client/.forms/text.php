<?php
// Creates an input element.
// Which works well for most input types
// that are text based.
/**
 * @var string $_form
 * @var string $_name
 * @var string|string[] $_label
 * @var mixed $_data
 * @var array $_rules
*/

//;
{
  global $P;

  $_form = $_form ?? '';
  $_name = $_name ?? '';
  $_type = $_type ?? '';
  $_label = $_label ?? '';
  $_data = $_data ?? '';
  $_rules = $_rules ?? [];

  if(is_string($_data)) {
    $_data = [ 'value'=>$_data, 'itype'=>'text' ];
  }
  $itype = $_data['itype'] ?? 'text';
  $value = $_data['value'] ?? '';

  $P
  ->form_element(['data-form'=>$_form,'data-name'=>$_name])
    ->auto_ui(['id'=>".$_form:$_name",'class'=>'ui-text','data-autoload'=>'InputUI'])
      ->input(['value'=>$value,'type'=>$itype,'placeholder'=>''])
      ->div('form-label')->ilabel($_label)->_div()
    ->_auto_ui()
    ->formRules($_rules)
    ->form_validator()
      ->text('something')
    ->_form_validator()
  ->_form_element()
  ;
}