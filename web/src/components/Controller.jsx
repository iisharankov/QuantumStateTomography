import React from 'react';
import { Formik } from 'formik';
import { Button } from '@material-ui/core';

import CustomTextField from './CustomTextField';
import Manager from './Manager';

// Allow user to select qubits to display
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
        <h3>Qubit Controller</h3>
        <Formik
          initialValues={{ quantity: this.state.quantity }}
          validate={this.validate}
          onSubmit={(data) => {
            this.setState({ quantity: data.quantity });
          }}
        >
          {({ handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <CustomTextField name="quantity" label="Number of Qubits" />
              <Button type="submit" variant="contained" color="primary">SUBMIT QUANTITY</Button>
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
