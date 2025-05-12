"use strict";

import ElementUI from '/.autoui/ui/ElementUI.js';

const SITE_ID = '2e323604-3828-4aca-a4d6-8a5405103370';

/**
 * AutoUI Captcha by hCaptcha class.
 * Data Type: string
 */
class CaptchaUI extends ElementUI {

  /** @param {CaptchaUI} c */
  static getOrWait(c) {
    // is here
    if(globalThis.hcaptcha) {
      c.onLoad();
      return;
    }

    // wait then
    let interval = undefined;
    interval = setInterval(() => {
      if(!globalThis.hcaptcha) return;
      c.onLoad();
      clearInterval(interval);
    }, 500);
  }

  /**
   * @param {HTMLElement} elm
   */
  constructor(elm) {
    super(elm);

    // get element
    this.container = elm.querySelector('.--container');
    
    /** @type {string|null} */
    this.widgetID = null;
    this.response = null;

    // catch hcaptcha
    CaptchaUI.getOrWait(this);
  }

  onLoad() {
    this.container.querySelectorAll('.--loading').forEach(elm => elm.remove());
    this.widgetID = globalThis.hcaptcha.render(
      this.container,
      {
        theme: "dark",
        sitekey: SITE_ID,
        'callback': (r) => this.onResponse(r),
        'expired-callback': () => this.onExpired(),
        'chalexpired-callback': () => this.onExpired(),
        'error-callback': () => this.onExpired(),
      }
    );
  }

  /**
   * @param {string} r
   */
  onResponse(r) {
    this.response = r;
    this.onchange && this.onchange();
  }

  onExpired() {
    this.reset();
  }

  reset() {
    globalThis.hcaptcha.reset(this.widgetID);
    this.response = null;
    this.onchange && this.onchange();
  }

  /**
   * @return {*}
   */
  getData() {
    return this.response;
  }

  /**
   * @param {*} value
   */
  setData(value) {
    this.reset();
  }

}

// ...
export default CaptchaUI;