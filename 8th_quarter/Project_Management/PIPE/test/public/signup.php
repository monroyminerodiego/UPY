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
    ],
    'scripts'=>[
      ['https://js.hcaptcha.com/1/api.js','async','defer']
    ]
  ])
  ->client('navbar')
  ->div('reglog-bg')
    ->div('float --border')
      ->div('p-2')

        ->formBegin('signup','/@accounts/Handler::signup')
        ->h4('mb-2')->text('Regístrate')->_h4()
        ->div('mb-2')
          ->formField('username','text',['fas fa-user mr-1','Usuario'],rules: [
            ['trim', null],
            ['minlen', 3, 'Debe tener al menos $0 caracteres.'],
            ['maxlen', 30, 'Debe tener a lo mucho $0 caracteres.'],
          ])
        ->_div()
        ->div('mb-2')
          ->formField('password','text',['fas fa-key mr-1','Contraseña'],['itype'=>'password'], [
            ['trim', null],
            ['minlen', 3, 'Debe tener al menos $0 caracteres.'],
            ['maxlen', 30, 'Debe tener a lo mucho $0 caracteres.'],
            ['notfield', 'username', 'No puede ser igual a tu nombre de usuario.'],
            ['poke', 'pw_repeat', null],
          ])
        ->_div()
        ->div('mb-2')
          ->formField('pw_repeat','text',['fas fa-key mr-1','Repite Contraseña'],['itype'=>'password'],[
            ['trim', null],
            ['minlen', 3, 'Debe tener al menos $0 caracteres.'],
            ['maxlen', 30, 'Debe tener a lo mucho $0 caracteres.'],
            ['eqfield', 'password', 'Las contraseñas no coinciden.'],
          ])
        ->_div()
        ->div('mb-2')
          ->formField('captcha','captcha',['fas fa-barcode mr-1', 'Captcha'], rules: [
            ['notnull', 'Por favor, resuelve el desafío.'],
          ])
        ->_div()
        ->div('u-right')
          ->button(['class'=>'m-0 btn-color-500 --green --ani','data-form-upload'=>'signup'])->text('Entrar')->_button()
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