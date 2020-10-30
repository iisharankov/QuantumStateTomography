import React from 'react';
import { Formik } from 'formik';
import { Button } from '@material-ui/core';

import CustomTextField from './singleQubitVisualizer/CustomTextField';
import HoC from './hoc';

// Optional component not in use
class RadialSelector extends React.Component {
  render() {
    return (
      <>
        <h3>Radial Qubit Selector</h3>
        <div id="image">
          {this.props.image ? <img alt="qubit" src={`data:image/png;base64,${this.props.image}`} /> : ''}
        </div>
        <Formik
          initialValues={{ radialX: 0, radialY: 0 }}
          validate={this.props.validate}
          onSubmit={(data, { setSubmitting }) => {
            this.props.onSubmit(data, 'radial', setSubmitting);
          }}
        >
          {({ values, isSubmitting, handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <CustomTextField name="radialX" label="Theta Angle" />
              <CustomTextField name="radialY" label="Phi Angle" />
              <Button disabled={isSubmitting} type="submit">SUBMIT QUBIT</Button>
            </form>
          )}
        </Formik>
      </>
    );
  }
}

const RadialSelectorExport = HoC(RadialSelector);

export default RadialSelectorExport;
