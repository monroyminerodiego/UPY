<?php
require_once __DIR__.'/../pipe/PIPE.php';
require_once __DIR__.'/../pipe/Printer.php';
require_once __DIR__.'/../pipe/FormRules.php';
//;
{
  global $P;

  $P
  ->client('header', [
    'title'=>'New Planet MC',
    'stylesheets'=>[
      '/main.css',
      '/reglog.css',
    ]
  ])
  ->client('navbar')
  ->div('reglog-bg')
    ->div('float --border')
      ->div('p-2')

        ->formBegin('login','/@accounts/Handler::login')
          ->h4('mb-2')->text('Inicia Sesión')->_h4()
          ->div('mb-2')
            ->formField('username','text',['fas fa-user mr-1','Usuario'],null,[
              ['maxlen', 10, 'Must be at least 10 characters long']
            ])
          ->_div()
          ->div('mb-2')
            ->formField('password','text',['fas fa-key mr-1','Contraseña'],['itype'=>'password'])
          ->_div()
          ->div('u-right')
            ->button('m-0 btn-color-500 --green --ani')->text('Entrar')->_button()
          ->_div()
        ->formEnd()

      ->_div()
    ->_div()
  ->_div()
  ->client('footer', [
    'scripts'=>[
    ]
  ])
  ;
}