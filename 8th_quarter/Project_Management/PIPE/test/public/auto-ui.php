<?php

use pipe\Printer;

require_once 'pipe/web/Printer.php';

//;
{
  global $P;
  $P->stylesheets(
    '/.fa/all.min.css',
    '/.pipe/pipus.css',
    '/.autoui/autoui.css'
  );

  $P
  ->div('p-4')
    ->div('p-4')->h2()->text('AutoUI demostration')->_h2()->_div()

    ->div('p-4')
      ->div()->text('select')->_div()
      ->autoui(['select',
        'id'=>'select-1',
        'selected'=>2,
        'options'=>['Option One','Option Two', 'Option Three but it\'s really big','Alright']
      ])
      ->div(['style'=>'max-width:12rem;'])
        ->autoui(['select',
          'id'=>'select-2',
          'selected'=>2,
          'options'=>['Option One','Option Two', 'Option Three but it\'s really big','Alright']
        ])
      ->_div()
    ->_div()

    ->div('p-4')
      ->div()->text('toggle')->_div()
      ->autoui(['toggle', 'checked'=>false,])
    ->_div()

    ->div('p-4')
      ->div()->text('toggle w/ label')->_div()
      ->autoui(['toggle', 'checked'=>true, 'width'=>'3rem', 'labels'=>['Y', 'N'] ])
    ->_div()

    ->div('p-4')
      ->div()->text('input (text)')->_div()
      ->autoui(['text'])
    ->_div()

    ->div('p-4')
      ->div()->text('input (password)')->_div()
      ->autoui(['text','type'=>'password'])
    ->_div()

    ->div('p-4')
      ->div()->text('input (color)')->_div()
      ->autoui(['text','type'=>'color'])
    ->_div()

    ->div('p-4')
      ->div()->text('buttons')->_div()
      ->div()
        ->button('--ani')->text('button')->_button()
      ->_div()
      ->exe(function(Printer $P) {
        foreach(['pink','red','orange','yellow','green','teal','blue','indigo','purple','gray'] as $color) {
          $P->div('u-flex');
          foreach([100, 300, 500, 700, 900] as $shade) {
            $P
            ->button(['class'=>"btn-color-$shade --$color --ani u-flex-grow-1"])
              ->text("$color $shade button")
            ->_button()
            ;
          }
          $P->_div();
        }
      })
    ->_div()

    ->div('p-4')
      ->div()->text('tabs (only one can be active)')->_div()
      ->div(['data-autoload'=>'Slides'])
      ->_div()
    ->_div()

    ->div('p-4')
      ->div()->text('slides (only one can be shown)')->_div()
      ->div(['data-autoload'=>'Slides'])
      ->_div()
    ->_div()

    ->div('p-4')
      ->div()->text('file, small-file, and their previews (general, image, audio, video)')->_div()
      ->div(['data-autoload'=>'Slides'])
      ->_div()
    ->_div()

  ->_div()
  ;

  $P->scripts('/.autoui/autoui.js');
}