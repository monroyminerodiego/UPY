"use strict";

import ElementUI from '/.autoui/ui/ElementUI.js';

/**
 * AutoUI Select class.
 * Data Type: string
 */
class SelectUI extends ElementUI {

  /**
   * @param {HTMLElement} elm
   */
  constructor(elm) {
    super(elm);
    this.index = -1;
    this.value = elm.dataset.selected || null;
    this.optcont = elm.querySelector('.dropdown .wrapper');
    this.options = [...elm.querySelectorAll('.dropdown .wrapper > div.option')];
    this.display = elm.querySelector('.border .background .container .display');
    this.default = this.display.firstChild.cloneNode(true);
    this.basecl = elm.classList;
    this.options.forEach(elm => elm.onclick = () => this.onoptclick(elm));
    this.base.onclick = ev => this.onclick(ev);
    document.addEventListener('click', ev => this.onglobalclick(ev));
  }

  /** @param {MouseEvent} ev */
  onglobalclick(ev) {
    // NOT INSIDE
    if(ev.target == this.base || this.base.contains(ev.target)) return;
    this.basecl.remove('active');
  }

  /** @param {MouseEvent} ev */
  onclick(ev) {
    // NOT INSIDE OPTIONS
    if(ev.target == this.optcont || this.optcont.contains(ev.target)) return;
    this.basecl.toggle('active');
  }

  /** @param {HTMLElement} elm */
  onoptclick(elm) {
    this.value = elm.dataset.value || null;
    this.basecl.remove('active');
    this.update();
  }

  // Visual Update
  update() {
    let found = false;
    let f_elm = null;

    // loop to find the selected one
    for(let i = 0; i < this.options.length; i++) {
      const v = this.options[i];
      let v_val = v.dataset.value;
      let match = v_val == this.value;
      if(f_elm == null && match) f_elm = v.firstChild;
      found |= match;
      v.classList[ match ? 'add' : 'remove' ]('active');
    }

    // now, replace the display with that element.
    if(f_elm == null) f_elm = this.default;
    f_elm = f_elm.cloneNode(true);
    this.display.replaceChildren([]);
    this.display.appendChild(f_elm);

    // check found
    if(!found) this.value = null;

    // ok..
    return found;
  }

  /**
   * @return {string}
   */
  getData() {
    return this.value;
  }

  /**
   * @param {string} value
   */
  setData(value) {
    // update...
    this.value = value;
    this.update();
  }

};

// ...
export default SelectUI;
