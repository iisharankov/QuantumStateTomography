import React from 'react';
import { Button, Grid, Slider, Typography } from '@material-ui/core';

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
        console.log(`data = ${Object.keys(data)}`);
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
    if (prevState.index !== this.state.index || prevState.cache !== this.state.cache) {
      loadQubits(this.state.cache, this.state.index);
    }

    const canvasObj = this.canvasRef.current;
    const ctx = canvasObj.getContext('2d');
    draw(ctx);
  }

  render() {
    return (
      <>
        <h3>Quantum Machine Learning Demo</h3>
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
            <Grid container item xs={2} >
              {
                this.state.error ? <h3>Error. Please change parameters.</h3> : ''
              }
            </Grid>
          </Grid>
        </Grid>
      </>
    );
  }

  phiCount() {
    if (this.state.cache === null) return 0;

    return Object.keys(this.state.cache.phis).length;
  }
}

export default QMLDemo;
