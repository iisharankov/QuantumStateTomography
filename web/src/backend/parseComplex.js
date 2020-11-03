import Complex from 'Complex';

function parseComplex(reply) {
  // Parse data for Quantum Machine Learning demo
  const { phis } = reply;

  for (let i = 0; i < phis.length; ++i) {
    let state = phis[i];
    for (const [key, value] of Object.entries(state)) {
      state[key] = Complex.from(value[0], value[1]);
    }
  }

  return reply;
}

export default parseComplex;
