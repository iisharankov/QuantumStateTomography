import React from 'react';
import { Button, Grid, Slider, Typography } from '@material-ui/core';

import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import post from '../backend/post';
import parseComplex from '../backend/parseComplex';
import { draw, CANVAS_SIZE, loadQubits } from '../lib/QMLCanvas';

class QMLDemo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cache: null,
      error: false,
      index: 0,
      loading: false,
      circ_depth: 10,
      num_qbits: 5,
      visual: 'Line',
    }

    this.canvasRef = React.createRef();
  }

  submit = () => {
    if (!this.state.loading) {
      this.setState({
        error: false,
        loading: true
      });

      const args = {
        circ_depth: this.state.circ_depth,
        num_qbits: this.state.num_qbits,
      };

      post('qml', args)
      .then(async (response) => {
        const reply = await response.json();

        if (reply === 'Error') {
          console.log('Error running QMLDemo.');
          throw reply;
        }

        const data = parseComplex(reply);
        this.setState({
          cache: data,
          loading: false,
        });
      })
      .catch((err) => {
        console.error(err);
        this.setState({
          error: true,
          loading: false,
        })
      });
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.cache !== null &&
      (prevState.index !== this.state.index || prevState.cache !== this.state.cache || prevState.visual !== this.state.visual)) {
      loadQubits(this.state.cache, this.state.index, this.state.visual);
    }

    const canvasObj = this.canvasRef.current;
    const ctx = canvasObj.getContext('2d');
    draw(ctx);
  }

  render() {
    return (
      <>
        <h2>Quantum Machine Learning Demo</h2>
        <p>Press start to generate a random quantum state. Calculations usually take about one minute so read the description below while it loads.</p>
        <Grid container xs={12} justify="flex-start" alignItems="flex-start">
          <Grid container item xs={12} >
            <canvas
            className="App-canvas"
            ref={this.canvasRef}
            width={CANVAS_SIZE}
            height={CANVAS_SIZE} />
          </Grid>
          <Grid container item xs={6} >
            <Typography id="discrete-slider-restrict" gutterBottom>
              Iteration
            </Typography>
            <Slider
            defaultValue={0}
            aria-labelledby="discrete-slider-small-steps"
            step={1}
            marks
            min={0}
            max={Math.max(0, this.phiCount() - 1)}
            valueLabelDisplay="auto"
            onChange={(event, value) => this.setState({index: value})}
            />
          </Grid>

          <Grid container item xs={12} spacing={3} >
            <Grid container item xs={2} >
              <Typography id="discrete-slider-restrict" gutterBottom>
                Circuit Depth
              </Typography>
              <Slider
              defaultValue={10}
              aria-labelledby="discrete-slider-small-steps"
              step={1}
              marks
              min={1}
              max={10}
              valueLabelDisplay="auto"
              onChange={(event, value) => this.setState({circ_depth: value, error: false})}
              />
            </Grid>
            <Grid container item xs={2} >
              <Typography id="discrete-slider-restrict" gutterBottom>
                Number of Qubits
              </Typography>
              <Slider
              defaultValue={5}
              aria-labelledby="discrete-slider-small-steps"
              step={1}
              marks
              min={1}
              max={6}
              valueLabelDisplay="auto"
              onChange={(event, value) => this.setState({num_qbits: value, error: false})}
              />
            </Grid>
            <Grid container item xs={1} >
              <Button disabled={this.state.loading || this.state.error} type="button" onClick={this.submit}
                variant="contained" color="primary">START</Button>
            </Grid>
            <Grid container item xs={1} >
              <FormControl>
                <InputLabel>Visual</InputLabel>
                <Select
                  onChange={(event, value) => {
                    this.setState({visual: event.target.value});
                  }}
                >
                  <MenuItem value="Line">Line</MenuItem>
                  <MenuItem value="Trail">Trail</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid container item xs={2} >
              {
                this.state.error ? <h3>Error. Please change parameters.</h3> : ''
              }
            </Grid>
          </Grid>
        </Grid>
        <p>A quantum state can be represented as 2^n complex coefficients where the absolute value is between 0 and 1. Where n is the number of qubits.</p>
        <p>There are many different ways to visualize these coefficients. We have graph each coefficient on a unit circle in the complex plane (scaled so the radius is that of the magnitude of the largest coefficient.) As the model stabilizes you will notice coloured dots slowly settle where the original is likely to remain. If you are observant you may notice the model will rarely and seemingly converge on a quantum state before changing to a drastically new one. Careful observation would show these solutions are nearly identical and are phase shifts of each other. Global phase shifts are represented as clockwise or counterclockwise rotations of all dots.</p>
        <p>The Line visual draws each point from the origin. The Trail visual will draw indicators for the past and future positions of each coefficient in adjacent iterations. How do the visuals change as the model steadies?</p>
        <p>Iteration: The number of cycles the machine learning model will try before converging on the desired state.</p>
        <p>Circuit Depth: The complexity of the circuit. Greater depth increases accuracy and runtime.</p>
        <p>Number of Qubits: Careful; this increases exponentially!</p>
      </>
    );
  }

  phiCount() {
    if (this.state.cache === null) return 0;

    return Object.keys(this.state.cache.phis).length;
  }
}

export default QMLDemo;
