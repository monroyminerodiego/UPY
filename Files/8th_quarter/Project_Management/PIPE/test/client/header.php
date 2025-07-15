<?php
/**
 * @var string $_title
 * @var string[] $_stylesheets
 * @var string[] $_scripts
 */
//;
{
  global $P;
  $_title = $_title ?? '';
  $_stylesheets = $_stylesheets ?? [];
  $_scripts = $_scripts ?? [];
  $P
  ->html()
    ->head()
      ->title()->text($_title)->_title()
      ->stylesheets(
        '/.pipe/pipus.css',
        '/.fa/all.min.css',
        '/.autoui/autoui.css',
        '/.autoui/forms.css',
      )
      ->stylesheets(...$_stylesheets)
      ->scripts(...$_scripts)
    ->_head()
    ->body()
      ->div('main')
  ; 
}