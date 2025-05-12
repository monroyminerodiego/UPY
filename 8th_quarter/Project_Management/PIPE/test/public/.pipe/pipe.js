"use strict";

/**
 * @param {string} selector
 * @returns {HTMLElement|HTMLElement[]}
 */
function q(selector) {
  let r = [...document.querySelectorAll(selector)];
  return r.length == 1 ? r[0] : r;
}