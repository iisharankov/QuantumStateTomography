import { Field, useField } from 'formik';
import { TextField } from '@material-ui/core';

const CustomTextField = ({ label, ...props }) => {
  const [field, meta] = useField(props);
  const errorText = meta.error && meta.touched ? meta.error : '';

  return (
    <Field
      {...field}
      as={TextField}
      error={errorText}
      helperText={errorText}
      label={label}
      size="small"
      type="number"
    />
  );
};

export default CustomTextField;
