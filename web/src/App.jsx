import React from 'react';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

import Controller from './components/singleQubitVisualizer/Controller';
import QMLDemo from './components/QMLDemo';


function App() {
  const darkTheme = createMuiTheme({
    palette: {
      type: 'dark',
    },
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ].join(','),
      fontSize: 18,
    },
  });

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline/>
        <div style={{marginLeft: "50px"}} >
          <Controller />
          <br></br>
          <br></br>
          <hr></hr>
          <br></br>
          <QMLDemo />
          <br></br>
          <br></br>
          <hr></hr>
          <br></br>
          <h3>Why Quantum?</h3>
          <p>Quantum computers can solve problems classical computers could never come close to simulating. Simulating protein folding would allow for modelling drugs and disease; potentially opening up a cure to cancer in the far future. Similarly, the ability to model complex molecules and lattices will dramatically advance material science leading to a world of smart materials and prolific nanotechnology.</p>
          <p>The first step to making a quantum computer is measuring, understanding, and predicting quantum states. Only through quantum state tomagraphy can we begin designing computers using the power of light or atoms.</p>
        </div>
    </ThemeProvider>
  );
}

export default App;
