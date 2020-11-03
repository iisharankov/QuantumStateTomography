import React from 'react';
import { Formik } from 'formik';
import { Button, Grid } from '@material-ui/core';

import CustomTextField from './CustomTextField';
import Manager from './Manager';

// Allow user to select qubits to single qubit visualizer
class Controller extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      quantity: 1,
    };
  }

  render() {
    return (
      <>
        <h2>Single Qubit Visualizer</h2>
        <p>Use this module to visualize qubits on the bloch sphere. Note all states here are static. This module is independent from the one below.</p>
        <p>What constraints can you find on the coefficients? Does a global phase on |0> and |1> change the depiction of the qubit?</p>
        <p>A single bit can only store 0 or 1. How many possible values can be created here?</p>
        <p>First select the number of qubits you wish you visualize. Note that pressing SUBMIT will automatically NORMALIZE your coefficients.</p>
        <Formik
          initialValues={{ quantity: this.state.quantity }}
          validate={this.validate}
          onSubmit={(data) => {
            this.setState({ quantity: data.quantity });
          }}
        >
          {({ handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <Grid container item xs={12} spacing={3} >
                <Grid container item xs={2} >
                  <CustomTextField name="quantity" label="Number of Qubits" />
                </Grid>
                <Grid container item xs={2} >
                  <Button type="submit" variant="contained" color="primary">SUBMIT QUANTITY</Button>
                </Grid>
              </Grid>
            </form>
          )}
        </Formik>
        <Manager quantity={this.state.quantity} />
      </>
    );
  }

  validate(values) {
    const errors = {};
    const value = values.quantity;

    if (isNaN(value)) {
      errors.quantity = 'Insert a number.';
    } else if (value < 0) {
      errors.quantity = 'Select a quantity greater than 0.';
    }

    return errors;
  }
}

export default Controller;
