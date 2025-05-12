"use strict";

import ElementUI from '/.autoui/ui/ElementUI.js';

class FormField {

  /**
   * @param {FormUI} form
   * @param {HTMLElement} fe
   * @param {ElementUI} ui 
   */
  constructor(form, fe, ui) {
    this.form = form;
    this.fe = fe;
    this.ui = ui;
    this.ui.onchange = () => this.onchange();
    this.fevalid = fe.querySelector('form-validator');
    this.rules = JSON.parse(fe.querySelector('form-rules').textContent);
  }

  onchange() {
    this.validate();
  }

  validate() {
    let data = this.ui.getData();
    const rules = this.rules;
    //console.log(rules);

    for(let i = 0; i < rules.length; i++) {
      const args = [...rules[i]];
      const fun = args.shift();
      /** @type {string} */
      let msg = args.pop();
      const r = FormRules[fun](this.form, data, args);

      // may be array?
      //console.log('->', r, i, data);
      if(Array.isArray(r)) {
        data = r[0];
        continue;
      }

      // ok, is boolean
      if(r) {
        this.message(null);
      } else {
        args.forEach((v, i) => {
          msg = msg.replace(`$${i}`, `${v}`);
        });
        this.message(msg);
        return false;
      }
    }

    return true;
  }

  message(msg) {
    if(msg)
      this.fe.classList.add('validator');
    else {
      this.fe.classList.remove('validator');
      return;
    }
    this.fevalid.textContent = msg;
  }

}

class FormRules {

  static trim(form, data, args) {
    return [data.trim()];
  }

  static minlen(form, data, args) {
    return data.length >= args[0];
  }

  static maxlen(form, data, args) {
    return data.length <= args[0];
  }

  static notnull(form, data, args) {
    return !!data;
  }

  /** @param {FormUI} form */
  static notfield(form, data, args) {
    return data != form.get(args[0]);
  }

  /** @param {FormUI} form */
  static eqfield(form, data, args) {
    return data == form.get(args[0]);
  }

  /** @param {FormUI} form */
  static poke(form, data, args) {
    form.fields[args[0]].validate();
    return true;
  }

}

/**
 * AutoUI Form Class
 */
class FormUI extends ElementUI {

  /**
   * @param {HTMLElement} elm
   */
  constructor(elm) {
    super(elm);
    const ds = elm.dataset;
    this.name = ds.name;
    this.upload = ds.upload;
    this.fields = {};
    this.base.querySelectorAll(`form-element[data-form="${this.name}"]`).forEach(elm => {
      const ds = elm.dataset;
      this.fields[ds.name] = new FormField(this, elm, autoui[`.${this.name}:${ds.name}`]);
    });
    this.buttons = [...document.querySelectorAll(`[data-form-upload="${this.name}"]`)];
    this.buttons.forEach(b => b.onclick = () => this.submit());
  }

  submit() {
    //console.log('submitting...');
    if(!this.validate()) return;
    this.submitStatic();
  }

  /**
   * Submits the form using a single request.
   */
  submitStatic() {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', this.upload, true);
    xhr.onprogress = (ev) => this.onprogress(ev);
    xhr.onloadstart = (ev) => this.onstart(xhr);
    xhr.onloadend = (ev) => this.onend(xhr);
    xhr.onload = (ev) => this.onsuccess(xhr);
    xhr.onerror = (ev) => this.onerror(xhr);
    xhr.send(this.formdata());
  }

  /** @param {ProgressEvent<EventTarget>} ev */
  onprogress(ev) {}

  /** @param {XMLHttpRequest} xhr */
  onstart(xhr) {}

  /** @param {XMLHttpRequest} xhr */
  onend(xhr) {}

  /** @param {XMLHttpRequest} xhr */
  onerror(xhr) {}

  /** @param {XMLHttpRequest} xhr */
  onsuccess(xhr) {
    this.postProcessing(JSON.parse(xhr.response));
  }

  formdata() {
    const fd = new FormData();
    const data = this.getData();
    for(let k in data) {
      fd.set(k, data[k]);
    }
    return fd;
  }

  /**
   * @return {*}
   */
  getData() {
    let out = {};
    for(let k in this.fields) {
      out[k] = this.fields[k].ui.getData();
    }
    return out;
  }

  /**
   * @param {*} value
   */
  setData(value) {}

  /** @param {string} field */
  get(field) {
    return this.fields[field].ui.getData();
  }

  validate() {
    let result = true;
    for(let k in this.fields) {
      result &= this.fields[k].validate();
    }
    return result;
  }

  /**
   * @param {{}} response
   */
  postProcessing(response) {
    // .fields
    response.fields && response.fields.forEach(f => {
      // .name
      const field = this.fields[f.name];
      // .status
      // .message
      field.message(f.message);
    });

    // .success
    // .message
  }

}

// ...
export default FormUI;
