<?php
require_once __DIR__.'/../../pipe/PIPE.php';

global $PIPE_DIR;
require_once $PIPE_DIR.'/Printer.php';
require_once $PIPE_DIR.'/FormRules.php';

//;
{
  global $P;

  $P
  ->client('header', [
    'title'=>'New Planet MC',
    'stylesheets'=>[
      '/main.css',
      '/user/user.css'
    ]
  ])
  ->client('navbar')
  ->div('main-content account')

    ->div('banner')
      ->img(['src'=>'/imgs/landscape.jpg'])
    ->_div()

    ->div('top')
      ->div('--right')->_div()
      ->div('--center nameplate')
        ->div('pfp')
          ->icon('fas fa-user')
        ->_div()
        ->div('username')->h2()->text('Username')->_h2()->_div()
      ->_div()
      ->div('--left')
        ->div()->text('Sesión')->_div()
        ->div()->text('Ajustes')->_div()
        ->div()->text('...')->_div()
      ->_div()
    ->_div()
    
    ->div('middle')
    ->_div()
    
    ->div('bottom')
      ->text('Bottom Text')
    ->_div()
    
  ->_div()
  ->client('footer', [
    'scripts'=>[
    ]
  ])
  ;
}