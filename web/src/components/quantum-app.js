import { LitElement, html } from 'lit';
import './qubit-visualizer.js';
import './qml-demo.js';

export class QuantumApp extends LitElement {
  createRenderRoot() {
    return this; // No shadow DOM - use global styles
  }

  render() {
    return html`
      <div class="sections-grid">
        <qubit-visualizer></qubit-visualizer>
        <qml-demo></qml-demo>
      </div>

      <hr>

      <h3>Why Quantum?</h3>
      <p>Quantum computers can solve problems classical computers could never come close to simulating. Simulating protein folding would allow for modelling drugs and disease; potentially opening up a cure to cancer in the far future. Similarly, the ability to model complex molecules and lattices will dramatically advance material science leading to a world of smart materials and prolific nanotechnology.</p>
      <p>The first step to making a quantum computer is measuring, understanding, and predicting quantum states. Only through quantum state tomography can we begin designing computers using the power of light or atoms.</p>
    `;
  }
}

customElements.define('quantum-app', QuantumApp);
