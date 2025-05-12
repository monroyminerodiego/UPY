<?php
/**
 * @var string $_form
 * @var string $_name
 */
//;
{
  global $P;

  $_form = $_form ?? '';
  $_name = $_name ?? '';

  $P
  ->form_element(['data-form'=>$_form,'data-name'=>$_name])
    ->auto_ui(['id'=>".$_form:$_name",'class'=>'ui-captcha','data-autoload'=>'CaptchaUI'])
      ->div('form-label')->ilabel($_label)->_div()
      ->div(['class'=>'pt-2 --container'])
        ->div('--loading')
          ->ilabel(['fas fa-spinner fa-spin mr-1', 'Cargando...'])
        ->_div()
      ->_div()
    ->_auto_ui()
    ->formRules($_rules)
    ->form_validator()
      ->text('something')
    ->_form_validator()
  ->_form_element()
  ;
}