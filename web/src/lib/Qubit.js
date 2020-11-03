import Complex from 'Complex';
import QuantumCoefficient from './QuantumCoefficient';

export class Qubit {
  constructor(zero, one) {
    this.zero = zero;
    this.one = one;
  }

  export() {
    return [...this.zero.exportLinear(), ...this.one.exportLinear()];
  }

  exportForm() {
    // Not implemented
    const theta = 0;
    const phi = 0;

    const form = {
      r0: this.zero.real(),
      i0: this.zero.im(),
      r1: this.one.real(),
      i1: this.one.im(),
      theta,
      phi,
    };

    return form;
  }

  normalize() {
    // Normalize and set angle to 0
    const combinedLength = Math.sqrt((this.zero.magnitude() ** 2) + (this.one.magnitude() ** 2));
    const newAngle = this.one.angle() - this.zero.angle();

    const nZero = this.zero.normalize(this.zero.magnitude() / combinedLength);
    const nOne = this.one.normalize(this.one.magnitude() / combinedLength);

    const zero = nZero.setAngle(0);
    const one = nOne.setAngle(newAngle);

    return new Qubit(zero, one);
  }

  print() {
    console.log(`Qubit: ${JSON.stringify(this.exportForm())}`);
  }

  toString() {
    let output = '';

    const { zero } = this;
    const { one } = this;

    const zeroOut = `(${zero.prettyString()}) |0>`;
    const oneOut = `(${one.prettyString()}) |1>`;

    if (zero.magnitude() && one.magnitude()) {
      output = `${zeroOut} + ${oneOut}`;
    } else if (zero.magnitude()) {
      output = zeroOut;
    } else if (one.magnitude()) {
      output = oneOut;
    }
    return output;
  }

  updateForm(form) {
    const zero = new QuantumCoefficient(Number(form.r0), Number(form.i0));
    const one = new QuantumCoefficient(Number(form.r1), Number(form.i1));

    return new Qubit(zero, one).normalize();
  }
}

export function newQubit() {
  return new Qubit(new QuantumCoefficient(1, 0), new QuantumCoefficient(0, 0));
}

export function radialQubit(theta, phi) {
  const r0 = Math.cos(theta / 2);
  const zero = new QuantumCoefficient(r0, 0);

  const oneState = Complex.fromPolar(Math.sin(theta / 2), phi);
  const one = new QuantumCoefficient(oneState.real, oneState.im);

  return new Qubit(zero, one).normalize();
}
