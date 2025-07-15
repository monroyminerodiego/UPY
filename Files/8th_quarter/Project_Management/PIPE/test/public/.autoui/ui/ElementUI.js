/**
 * UI base element class for AutoUI.
 */
class ElementUI {

  /**
   * @param {HTMLElement} elm
   */
  constructor(elm) {
    this.base = elm;
    this.data = elm.dataset;
    this.onchange = undefined;
  }

  /**
   * Releases control over the element.
   */
  unload() {}

  reset() {}

  /**
   * @return {*}
   */
  getData() {
    return null;
  }

  /**
   * @param {*} value
   */
  setData(value) {
    // ..
  }

}

// ...
export default ElementUI;