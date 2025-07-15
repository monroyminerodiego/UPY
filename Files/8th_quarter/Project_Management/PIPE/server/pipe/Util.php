<?php

namespace pipe;

/*
 * General Utilities
*/

/**
 * Shifts the array, but
 * does not reindex it
 */
function array_shift_alt(array &$array) {
  $k = array_key_first($array);
  if ($k === null) return null;
  $v = $array[$k];
  unset($array[$k]);
  return $v;
}

/**
 * Fast check, doesn't bother to check every single entry.
 */
function is_array_array($what) {
  if(!is_array($what)) return false;
  $count = count($what);
  if($count == 0) return true;
  return is_array($what[0]) && is_array($what[$count - 1]);
}

/**
 * Lazy, fast check.
 */
function is_associative(array &$a):bool {
  if(empty($a)) return true;
  return is_string(array_key_first($a));
}

function flat_url(string $str): string {
  return urlencode(str_replace(' ', '-', mb_strtolower($str)));
}


/*
 * Encoders & Decoders for various formats.
*/

/**
 * Encodes as urlencode, but
 * uses another character
 */
function alt_urlencode(string $s, string $c = '&') {
  // get hex
  $hex = str_pad(strval(ord($c)), 2, '0', STR_PAD_LEFT);
  // encode as usual
  $s = urlencode($s);
  // replace the $c for "$c$hex"
  $s = str_replace($c, "$c$hex", $s);
  // replace the % for $c
  $s = str_replace('%', $c, $s);
  return $s;
}

/**
 * Decodes as urldecode, but
 * uses another character
 */
function alt_urldecode(string $s, string $c = '&') {
  // replace the $c for %
  $s = str_replace($c, '%', $s);
  // decode as usual
  $s = urldecode($s);
  return $s;
}

function base64url_encode(string $str): string {
  return strtr(base64_encode($str), '+/', '-_');
}

function base64url_decode(string $str): string {
  return base64_decode(strtr($str, '-_', '+/'));
}

function jsonEncode($value): string {
  return json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}

function jsonDecode(string $value) {
  return json_decode($value, false);
}

function jsonSave(string $path, $value) {
  ensureDir(dirname($path));
  file_put_contents($path, jsonEncode($value));
}

function jsonLoad(string $path) {
  return jsonDecode(file_get_contents($path));
}

function in_range(int $min, int $x, int $max) {
  return $min <= $x && $x <= $max;
}

/**
 * Throws an exception if the condition
 * is not true.
 * @throws Exception
 */
function ensure(bool $condition, string $msg) {
  if ($condition) return;
  throw new \Exception($msg);
}

/**
 * Ensures that a directory exists.
 * @return string The same path.
 */
function ensureDir(string $path): string {
  if (\file_exists($path)) return $path;
  \mkdir($path, 0777, true);
  return $path;
}

/**
 * Ensures that a file exists.
 * @return string The same file.
 */
function ensureFile(string $path, string $conts): string {
  ensureDir(\dirname($path));
  if (\file_exists($path)) return $path;
  \file_put_contents($path, $conts);
  return $path;
}

function deleteFiles($regex) {
  $files = \glob($regex);
  foreach ($files as $file) { // iterate files
    if (\is_file($file)) \unlink($file);
  }
}

/**
 * Sets a cookie.
 * @param int $expires Expiration date in seconds.
 */
function setCookie(string $key, string $value, int $expires) {
  $r = \setcookie($key, $value, $expires, '/');
  ensure($r, "Could not send cookie \"$key\".");
}

function getCookie(string $key): ?string {
  return $_COOKIE[$key] ?? null;
}

/**
 * Garantees that the function passed will be
 * executed syncronized with every other
 * thread.
 */
function synchronized(int $id, callable $function) {
  // windows does not have this
  if (!function_exists('sem_get')) require_once __DIR__ . '/winsem.php';

  // get the semaphore & lock
  $sem = \sem_get($id);
  if ($sem !== false) {
    \sem_acquire($sem);
    // call the function
    $function();
    // release & remove it
    \sem_release($sem);
    \sem_remove($sem);
  } else {
    // no luck, just call the thing
    $function();
  }
  // end
}
