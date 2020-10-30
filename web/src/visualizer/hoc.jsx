import React from 'react';

import getImg from '../backend/img';
import post from '../backend/post';

function HoC(WrappedComponent) {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        image: null,
      };
      this.onSubmit.bind(this);
    }

    onSubmit(data, id, setSubmitting) {
      setSubmitting(true);
      post(id, data)
        .then(async (response) => {
          this.setState({ image: await getImg(response) });
          setSubmitting(false);
        })
        .catch(() => setSubmitting(false));
    }

    render() {
      return <WrappedComponent onSubmit={this.onSubmit} image={this.state.image} validate={this.validate} />;
    }

    validate(values) {
      const errors = {};

      for (const [key, value] of Object.entries(values)) {
        if (isNaN(value)) {
          errors[key] = 'Insert a number.';
        } else if (value < 0) {
          errors[key] = 'Select a quantity greater than 0.';
        }
      }

      return errors;
    }
  };
}

export default HoC;
