"use strict";

import ElementUI from '/.autoui/ui/ElementUI.js';

/**
 * AutoUI Input class.
 * Data Type: string
 */
class InputUI extends ElementUI {

  /**
   * @param {HTMLElement} elm
   */
  constructor(elm) {
    super(elm);

    // get the element
    /** @type {HTMLInputElement} */
    this.input = elm.tagName == 'input' ? elm : elm.querySelector('input');

    // default field to edit
    this.field = 'value';

    // check type of element
    if(this.input.type == 'checkbox') this.field = 'checked';
    this.input.oninput = () => this.onchange && this.onchange();
  }

  /**
   * @return {*}
   */
  getData() {
    return this.input[this.field];
  }

  /**
   * @param {*} value
   */
  setData(value) {
    this.input[this.field] = value;
  }

}

// ...
export default InputUI;
