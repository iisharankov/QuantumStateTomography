import { LitElement, html } from 'lit';

import post from '../backend/post.js';
import parseComplex from '../backend/parseComplex.js';
import { draw, CANVAS_SIZE } from '../lib/QMLCanvas.js';

export class QMLDemo extends LitElement {
  static properties = {
    cache: { type: Object },
    error: { type: Boolean },
    index: { type: Number },
    loading: { type: Boolean },
    circDepth: { type: Number },
    numQbits: { type: Number },
    visual: { type: String }
  };

  constructor() {
    super();
    this.cache = null;
    this.error = false;
    this.index = 0;
    this.loading = false;
    this.circDepth = 10;
    this.numQbits = 5;
    this.visual = 'Line';
    this._resizeObserver = null;
  }

  createRenderRoot() {
    return this; // No shadow DOM
  }

  firstUpdated() {
    const canvas = this.querySelector('canvas');

    // Set up ResizeObserver for canvas
    this._resizeObserver = new ResizeObserver(() => {
      this._redrawCanvas();
    });

    if (canvas) {
      this._resizeObserver.observe(canvas);
      this._setCanvasDimensions();
    }

    // Don't auto-fetch - user must click START button
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    if (this._resizeObserver) {
      this._resizeObserver.disconnect();
    }
  }

  updated(changedProperties) {
    if (changedProperties.has('cache') ||
        changedProperties.has('index') ||
        changedProperties.has('visual')) {
      this._redrawCanvas();
    }

    // No auto-fetch on param changes - user must click START button
  }

  _setCanvasDimensions() {
    const canvas = this.querySelector('canvas');
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const size = Math.min(rect.width, CANVAS_SIZE);
    canvas.width = size;
    canvas.height = size;
  }

  _redrawCanvas() {
    const canvas = this.querySelector('canvas');
    if (!canvas) return;

    this._setCanvasDimensions();
    const ctx = canvas.getContext('2d');

    const canvasState = this.cache ? {
      allData: this.cache,
      index: this.index,
      visual: this.visual
    } : null;

    draw(ctx, canvasState);
  }

  _handleStart() {
    this._fetchQMLData();
  }

  async _fetchQMLData() {
    if (this.loading) return;

    this.error = false;
    this.loading = true;

    try {
      const response = await post('qml', {
        circ_depth: this.circDepth,
        num_qbits: this.numQbits
      });

      const reply = await response.json();

      if (reply === 'Error') {
        throw new Error('QML computation failed');
      }

      const data = parseComplex(reply);
      this.cache = data;
      this.index = 0;
    } catch (err) {
      console.error('QML Demo error:', err);
      this.error = true;
    } finally {
      this.loading = false;
    }
  }

  _getPhiCount() {
    return this.cache ? Object.keys(this.cache.phis).length : 0;
  }

  render() {
    return html`
      <h2>Quantum Machine Learning Demo</h2>
      <p>Adjust circuit parameters and click START to compute. Warning: This computation takes several minutes.</p>

      <canvas></canvas>

      <div style="display: flex; flex-wrap: wrap; gap: var(--app-gap); margin-block: var(--app-gap); align-items: end;">
        <div style="flex: 1; min-width: 200px;">
          <sl-range
            label="Circuit Depth"
            min="1"
            max="10"
            value="${this.circDepth}"
            @sl-input="${(e) => this.circDepth = parseInt(e.target.value)}"
            help-text="Greater depth = more accuracy, longer runtime"
            ?disabled="${this.loading}"
          ></sl-range>
        </div>

        <div style="flex: 1; min-width: 200px;">
          <sl-range
            label="Number of Qubits"
            min="1"
            max="6"
            value="${this.numQbits}"
            @sl-input="${(e) => this.numQbits = parseInt(e.target.value)}"
            help-text="Careful: increases exponentially!"
            ?disabled="${this.loading}"
          ></sl-range>
        </div>

        <div style="flex: 0; min-width: 120px;">
          <sl-button
            variant="primary"
            size="large"
            @click="${this._handleStart}"
            ?loading="${this.loading}"
            ?disabled="${this.loading}"
          >
            ${this.loading ? 'Computing...' : 'START'}
          </sl-button>
        </div>
      </div>

      ${this.cache ? html`
        <div style="display: flex; flex-wrap: wrap; gap: var(--app-gap); margin-block: var(--app-gap);">
          <div style="flex: 1; min-width: 200px;">
            <sl-range
              label="Iteration"
              min="0"
              max="${Math.max(0, this._getPhiCount() - 1)}"
              value="${this.index}"
              @sl-input="${(e) => this.index = parseInt(e.target.value)}"
            ></sl-range>
          </div>

          <div style="flex: 0; min-width: 150px;">
            <sl-select
              label="Visual"
              value="${this.visual}"
              @sl-change="${(e) => this.visual = e.target.value}"
            >
              <sl-option value="Line">Line</sl-option>
              <sl-option value="Trail">Trail</sl-option>
            </sl-select>
          </div>
        </div>
      ` : ''}

      ${this.loading ? html`<p><em>Computing... This may take several minutes. Please wait.</em></p>` : ''}
      ${this.error ? html`<p style="color: var(--sl-color-danger-600);"><strong>Error. Try different parameters or check backend connection.</strong></p>` : ''}

      <p>A quantum state can be represented as 2^n complex coefficients where the absolute value is between 0 and 1. Where n is the number of qubits.</p>
      <p>There are many different ways to visualize these coefficients. We graph each coefficient on a unit circle in the complex plane (scaled so the radius is that of the magnitude of the largest coefficient.) As the model stabilizes you will notice coloured dots slowly settle where the original is likely to remain.</p>
      <p>The Line visual draws each point from the origin. The Trail visual will draw indicators for the past and future positions of each coefficient in adjacent iterations.</p>
      <p><strong>Fidelity</strong>: Similarity of predicted and desired (hidden) quantum states. 1 is a perfect match. Contrast with the Loss.</p>
    `;
  }
}

customElements.define('qml-demo', QMLDemo);
