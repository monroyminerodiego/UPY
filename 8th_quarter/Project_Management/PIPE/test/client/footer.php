<?php
/**
 * @var string[] $_scripts
 */
//;
{
  global $P;
  $_scripts = $_scripts ?? [];
  $P
      ->div('--content-filler')->_div()
      // <---
      ->div('footer-container')
        ->footer('footer')
          ->div('content')
            ->divider('divider')->_divider()
          ->_div()
          ->p('subtitle')->text('PIPE3 @ ', date('Y'))->_p()
        ->_footer()
      ->_div()
      // <---
    ->scripts(
      '/.pipe/pipe.js',
      '/.autoui/autoui.js',
    )
    ->scripts(...$_scripts)
    ->_body()
  ->_html()
  ;
}