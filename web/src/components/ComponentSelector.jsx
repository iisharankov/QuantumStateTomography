import React from 'react';
import { Formik } from 'formik';
import { Button } from '@material-ui/core';

import CustomTextField from './CustomTextField';
import HoC from '../visualizer/hoc';

class ComponentSelector extends React.Component {
  render() {
    return (
      <>
        <h3>Component Qubit Selector</h3>
        <div id="image">
          {this.props.image ? <img alt="qubit" src={`data:image/png;base64,${this.props.image}`} /> : ''}
        </div>
        <Formik
          initialValues={{
            r0: 1, i0: 0, r1: 0, i1: 0,
          }}
          validate={this.props.validate}
          onSubmit={(data, { setSubmitting }) => {
            this.props.onSubmit(data, 'multivector', setSubmitting);
          }}
        >
          {({ values, isSubmitting, handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <div className="inline">
                <CustomTextField name="r0" label="Real Part |0>" />
                <CustomTextField name="i0" label="Im Part |0>" />
                <CustomTextField name="r1" label="Real Part |1>" />
                <CustomTextField name="i1" label="Im Part |1>" />
                <Button disabled={isSubmitting} type="submit">SUBMIT QUBIT</Button>
              </div>

            </form>
          )}
        </Formik>
      </>
    );
  }
}

const ComponentSelectorExport = HoC(ComponentSelector);

export default ComponentSelectorExport;
