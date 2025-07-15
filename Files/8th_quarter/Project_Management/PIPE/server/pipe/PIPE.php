<?php
namespace pipe;

/*
 * /.==========.\   ==============   /.==========.\   /.==========
 * ||          ||         ||         ||          ||   ||
 * ||          ||         ||         ||          ||   ||
 * ||          ||         ||         ||          ||   ||
 * ||          ||         ||         ||          ||   ||
 * ||==========./         ||         ||==========./   ||==========
 * ||                     ||         ||               ||
 * ||                     ||         ||               ||
 * ||                     ||         ||               ||
 * ||                     ||         ||               ||
 * ||               ==============   ||               \.==========
 * 
 *                     A PHP LIBRARY COLLECTION
*/

/*
 * THIS LIBRARY REQUIRES: 
 *  - curl (general fetching)
 *  - gd (images)
 *  - mbstring (utf-8)
 *  - exif (images)
 *  - openssl (hashes)
*/

/*
 * Directories.
*/

$ROOT_DIR = dirname($_SERVER['DOCUMENT_ROOT']);
set_include_path(get_include_path() . PATH_SEPARATOR . $ROOT_DIR);

$SERVER_DIR = realpath($ROOT_DIR.'/server') or throw new \Exception('Directory "server" does not exist!');
$CLIENT_DIR = realpath($ROOT_DIR.'/client') or throw new \Exception('Directory "client" does not exist!');
$DATA_DIR   = realpath($ROOT_DIR.'/data')   or throw new \Exception('Directory "data" does not exist!');
$PUBLIC_DIR = realpath($ROOT_DIR.'/public') or throw new \Exception('Directory "public" does not exist!');

/*
 * Quick Require.
*/

/*
 * Logging Functions
 * TODO: fix accuracy
*/

function log(string $msg) {
  global $ROOT_DIR;
  $ex = new \Exception();
  $trace = $ex->getTrace();
  $last = (object) $trace[0];
  /*
  array (
    'file' => '...file.php',
    'line' => 51,
    'function' => 'upload',
    'class' => 'SubHandler',
    'type' => '::',
  ),
  */
  $file = $last->file;
  $pos = strpos($file, $ROOT_DIR);
  if($pos !== false) $file = substr($file, strlen($ROOT_DIR));
  $fn = ($last->class ?? '').($last->type ?? '').($last->function ?? '?');
  $line = $last->line ?? '?';
  error_log("[LOG] $file @ $fn # $line: \n$msg");
}

function export($value) {
  global $ROOT_DIR;
  $ex = new \Exception();
  $trace = $ex->getTrace();
  $last = (object) $trace[0];
  $file = $last->file;
  $pos = strpos($file, $ROOT_DIR);
  if($pos !== false) $file = substr($file, strlen($ROOT_DIR));
  $fn = ($last->class ?? '').($last->type ?? '').($last->function ?? '?');
  $line = $last->line ?? '?';
  $msg = var_export($value, true);
  error_log("[EXP] $file @ $fn # $line: \n$msg");
}