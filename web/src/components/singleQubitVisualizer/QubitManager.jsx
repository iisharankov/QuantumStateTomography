import React from 'react';
import { Formik } from 'formik';
import { Button, Grid } from '@material-ui/core';

import CustomTextField from './CustomTextField';

const FORM_LABEL = {
  r0: 'Real |0>',
  i0: 'Imaginary |0>',
  r1: 'Real |1>',
  i1: 'Imaginary |1>',
  theta: 'Theta (Radians)',
  phi: 'Phi (Radians)',
};

// Display and modify a single qubit
class QubitManager extends React.Component {
  getFormValues() {
    const form = {};

    for (const [key, value] of Object.entries(this.props.state.qubit.exportForm())) {
      form[key] = value.toFixed(3);
    }

    return form;
  }

  render() {
    return (
      <>
        <h3>
          Qubit
          {this.props.id}
        </h3>
        <Formik
          initialValues={{ ...this.getFormValues() }}
          enableReinitialize
          onSubmit={(data, { setSubmitting }) => {
            setSubmitting(true);
            this.props.setState(data, setSubmitting);
          }}
        >
          {({ values, handleSubmit }) => (
            <Grid container xs={12} justify="flex-start" alignItems="flex-start">
              <Grid container item xs={2}>
                {this.props.state.image ? <img alt="qubit" src={`data:image/png;base64,${this.props.state.image}`} /> : ''}
              </Grid>
              <Grid container item xs={1}>
                {['Linear', 'Equation'].map((value) => (
                  <Grid container item spacing={4}>
                    <Grid key={value} item><h3>{value}</h3></Grid>
                  </Grid>
                ))}
              </Grid>
              <Grid container item xs={8}>
                <form onSubmit={handleSubmit}>
                  <Grid container item spacing={4}>
                    {['r0', 'i0', 'r1', 'i1'].map((value) => (
                      <Grid key={value} item xs={2}>
                        <CustomTextField name={value} label={FORM_LABEL[value]} />
                      </Grid>
                    ))}
                  </Grid>
                  <Grid container item spacing={4}>
                    <Grid key="Equation" item xs={4}>
                      <Grid key="Equation" item><h3>{this.props.state.qubit.toString()}</h3></Grid>
                    </Grid>
                    <Grid key="Normalize" item xs={2}>
                      <Button onClick={() => this.props.normalize(values)} variant="contained" color="secondary">NORMALIZE</Button>
                    </Grid>
                    <Grid key="Submit" item xs={2}>
                      <Button type="submit" variant="contained" color="primary">SUBMIT</Button>
                    </Grid>
                  </Grid>
                </form>
              </Grid>
            </Grid>
          )}
        </Formik>
      </>
    );
  }

  validate(values) {
    const errors = {};

    return errors;
  }
}

export default QubitManager;
