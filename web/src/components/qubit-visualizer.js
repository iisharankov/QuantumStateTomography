import { LitElement, html } from 'lit';

import post from '../backend/post.js';
import getImg from '../backend/img.js';
import { newQubit } from '../lib/Qubit.js';

export class QubitVisualizer extends LitElement {
  static properties = {
    quantity: { type: Number },
    _qubitStates: { state: true }
  };

  constructor() {
    super();
    this.quantity = 1;
    this._qubitStates = [{ image: null, qubit: newQubit() }];
  }

  createRenderRoot() {
    return this;
  }

  willUpdate(changedProperties) {
    if (changedProperties.has('quantity')) {
      this._syncQubitArray();
    }
  }

  _syncQubitArray() {
    const current = this._qubitStates.length;

    if (this.quantity > current) {
      const newQubits = Array(this.quantity - current)
        .fill(null)
        .map(() => ({ image: null, qubit: newQubit() }));
      this._qubitStates = [...this._qubitStates, ...newQubits];
    } else if (this.quantity < current) {
      this._qubitStates = this._qubitStates.slice(0, this.quantity);
    }
  }

  _handleInput(index, field, e) {
    const value = parseFloat(e.target.value) || 0;

    // Update form data immediately (local state only)
    const updated = [...this._qubitStates];
    const form = updated[index].qubit.exportForm();
    form[field] = value;
    updated[index].qubit = updated[index].qubit.updateForm(form);
    this._qubitStates = updated;

    // Don't auto-fetch - wait for user to click UPDATE or NORMALIZE
  }

  _handleUpdate(index) {
    this._updateAndFetch(index);
  }

  _handleNormalize(index) {
    const updated = [...this._qubitStates];
    updated[index] = { ...updated[index], qubit: updated[index].qubit.normalize() };
    this._qubitStates = updated;
  }

  async _updateAndFetch(index) {
    const qubit = this._qubitStates[index].qubit;
    const data = qubit.exportForm();

    try {
      const response = await post('multivector', data);
      const image = await getImg(response);

      const updated = [...this._qubitStates];
      updated[index] = { ...updated[index], image };
      this._qubitStates = updated;
    } catch (err) {
      console.error('Failed to fetch qubit image:', err);
    }
  }

  _renderQubitForm(state, index) {
    const form = state.qubit.exportForm();
    const labels = {
      r0: 'Real |0>',
      i0: 'Imaginary |0>',
      r1: 'Real |1>',
      i1: 'Imaginary |1>'
    };

    return html`
      <div style="margin-block: var(--app-gap); padding: var(--app-gap); border: 1px solid var(--sl-color-neutral-700); border-radius: var(--sl-border-radius-medium);">
        <h3>Qubit ${index + 1}</h3>

        <div style="display: grid; grid-template-columns: 3fr 1fr; gap: var(--app-gap); align-items: start;">
          <div>
            ${state.image ? html`
              <img
                src="data:image/png;base64,${state.image}"
                alt="Qubit ${index + 1} Bloch sphere"
                style="width: 100%; max-width: 400px; height: auto; object-fit: contain;"
              />
            ` : html`<div style="width: 100%; max-width: 400px; aspect-ratio: 1;"></div>`}

            <div style="margin-block-start: 1rem;">
              <strong>Equation:</strong> ${state.qubit.toString()}
            </div>
          </div>

          <div>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              ${Object.entries(labels).map(([field, label]) => html`
                <sl-input
                  label="${label}"
                  type="number"
                  step="0.001"
                  .value="${form[field].toFixed(3)}"
                  @sl-input="${(e) => this._handleInput(index, field, e)}"
                ></sl-input>
              `)}
            </div>

            <div style="display: flex; gap: 0.5rem; margin-block-start: 1rem;">
              <sl-button
                variant="primary"
                size="small"
                @click="${() => this._handleUpdate(index)}"
              >Update Visualization</sl-button>
              <sl-button
                variant="neutral"
                size="small"
                @click="${() => this._handleNormalize(index)}"
              >Normalize</sl-button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  render() {
    return html`
      <h2>Single Qubit Visualizer</h2>

      <div style="margin-block: var(--app-gap);">
        <sl-input
          label="Number of Qubits"
          type="number"
          min="1"
          max="10"
          value="${this.quantity}"
          @sl-input="${(e) => this.quantity = parseInt(e.target.value) || 1}"
          style="max-width: 200px;"
        ></sl-input>
      </div>

      ${this._qubitStates.map((state, i) => this._renderQubitForm(state, i))}
    `;
  }
}

customElements.define('qubit-visualizer', QubitVisualizer);
