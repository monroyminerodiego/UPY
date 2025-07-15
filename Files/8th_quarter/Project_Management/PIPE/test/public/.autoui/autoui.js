"use strict";

/**
 * Auto UI Class
 */
class AutoUI {

  constructor() {
    AutoUI.instance = this;
    this.numericID = 0;
    this.components = {};
    this.loaded = [];
    this.uipath = '/.autoui/ui';
    this.loadAll();
  }

  /**
   * Finds and loads elements in sequential order.
   */
  async loadAll() {
    // prepare
    let elms = [...document.querySelectorAll('auto-ui,[data-autoload]')];

    // separate low normal high
    let orders = {
      'lowest': [],
      'low': [],
      'normal': [],
      'high': [],
      'highest': [],
    };
    elms.forEach(elm => {
      const ds = elm.dataset;
      let order = ds.loadorder || 'low';
      orders[order].push(elm);
    });

    // load all
    for(let k in orders) {
      let elms = orders[k];
      for(let i = 0; i < elms.length; i++) {
        await this.load(elms[i]);
      }
    }
  }

  /**
   * Load one element.
   * @param {HTMLElement} elm
   */
  async load(elm, ignoreCache = false) {
    // check if we need to load something
    let autoload = elm.dataset.autoload;
    if(autoload == null) return;

    // check if it's cached
    if(elm.dataset.autoid != undefined && !ignoreCache) return;

    // import the module
    try {
      // load
      const clazz = await this.module(autoload);
      const obj = new clazz(elm);

      // assign an id
      if(elm.id == '') {
        elm.id = `autoui${++this.numericID}`;
      }
      let id = elm.id;

      // unload previous
      if(Object.hasOwn(this.components, id)) {
        let old = this.components[id];
        if(old.unload) old.unload();
      }
      
      // store / restore
      this.components[id] = obj;
    } catch(ex) {
      console.log('AutoUI: Error when loading element with module "' + autoload + '".')
      console.error(ex);
    }
  }

  /**
   * @param {string} name
   */
  async module(name) {
    return (await import( `${this.uipath}/${name}.js` )).default;
  }

  /**
   * @param {AutoUI} target
   * @param {string} prop
   */
  get(target, prop) {
    if(Object.hasOwn(this.components, prop)) return this.components[prop];
    return this[prop];
  }

  proxy() {
    return new Proxy(this, this);
  }
  
}

// AUTO EXEC
const autoui = new AutoUI().proxy();

