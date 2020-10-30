import React from 'react';

import QubitManager from './QubitManager';

import getImg from '../backend/img';
import post from '../backend/post';
import { newQubit } from '../lib/quantum';

function makeQubitManager() {
  return {
    image: null,
    qubit: newQubit(),
  };
}

// Displays set of qubits
class Manager extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      managers: [],
    };
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.quantity === this.state.managers.length) {
      return;
    }

    const managers = [...this.state.managers]; // Shallow copy
    while (this.props.quantity > managers.length) {
      managers.push(makeQubitManager());
    }

    if (this.state.managers.length !== managers.length) {
      this.setState({ managers });
    }
  }

  render() {
    return (
      <>
        {
            this.state.managers.map((state, i) => {
              if (i >= this.props.quantity) return <></>;

              return (
                <QubitManager
                  id={i + 1}
                  key={i}

                  normalize={(data) => {
                    this.updateForm(i, data);
                  }}

                  setState={(data, setSubmitting) => {
                    this.updateForm(i, data);

                    console.log(`data = ${JSON.stringify(data)}`);
                    post('multivector', data)
                      .then(async (response) => {
                        const managers = [...this.state.managers]; // Shallow copy
                        managers[i].image = await getImg(response);

                        this.setState({ managers }, () => setSubmitting(false));
                      })
                      .catch(() => setSubmitting(false));
                  }}
                  state={state}
                />
              );
            })
        }
      </>
    );
  }

  updateForm(i, data) {
    const managers = [...this.state.managers]; // Shallow copy
    managers[i].qubit = this.state.managers[i].qubit.updateForm(data);
    this.setState({ managers });
  }

  validate(values) {
    const errors = {};

    return errors;
  }
}

export default Manager;
