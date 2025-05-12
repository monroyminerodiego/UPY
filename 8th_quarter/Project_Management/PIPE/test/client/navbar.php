<?php
//;

use pipe\Printer;
require_once 'pipe/Util.php';

{
  global $P;

  $_bar = [
    'home'=>'PIPE3',
    'left' => [
      ['icon'=>'fas fa-newspaper mr-1','text'=>'News'],
      ['icon'=>'fas fa-star mr-1',     'text'=>'Features'],
      ['icon'=>'fas fa-sliders mr-1', 'text'=>'Auto UI'],
    ],
    'right' => [],
  ];

  // ------------------

  // Pre compute links if they don't exist
  foreach(['left','center','right'] as $k) {
    if(!isset($_bar[$k])) $_bar[$k] = [];

    foreach($_bar[$k] as &$v) {
      if(!isset($v['link'])) $v['link'] = '/'.\pipe\flat_url($v['text']);
      unset($v);
    }
  }

  // Print!

  $P
  ->div('header-container')
    // ---
    ->div('header m-0')
      ->div('header-brand')
        ->a(['class'=>'nav-item','href'=>'/'])
          ->h6()->text($_bar['home'])->_h6()
        ->_a()
        ->div('nav-item nav-btn')
          ->span()->_span()
          ->span()->_span()
          ->span()->_span()
        ->_div()
      ->_div()
      ->div('header-nav')
        ->div('nav-left')
          ->for_each($_bar['left'], function(Printer $P, $k, array $v) {
            $P
            ->div('nav-item')
              ->a(['href'=>$v['link']])
                ->icon($v['icon'])
                ->text($v['text'])
              ->_a()
            ->_div()
            ;
          })
        ->_div()
        ->div('nav-right')
          ->for_each($_bar['right'], function(Printer $P, $k, array $v) {
            $P
            ->div('nav-item')
              ->a(['href'=>$v['link']])
                ->icon($v['icon'])
                ->text($v['text'])
              ->_a()
            ->_div()
            ;
          })
        ->_div()
      ->_div()
    ->_div()
    // ---
  ->_div()
  ;
}