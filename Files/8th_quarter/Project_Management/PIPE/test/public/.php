<?php

require_once 'pipe/web/Printer.php';
//;
{
  global $P;

  $P
  ->client('header', [
    'title'=>'PIPE3',
    'stylesheets'=>[
      '/main.css',
    ]
  ])
  ->client('navbar')
  ->div('u-center my-1')
    ->h1('m-0')->text('PIPE3')->_h3()
  ->_div()
  ->div('main-content')
    ->icon('fas fa-wrench mr-1')->text('Under construction...')
  ->_div()
  ->client('footer')
  ;
}