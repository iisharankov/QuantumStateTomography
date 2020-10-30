import HueAngleToRGB from './HueAngleToRGB';


const TAU = Math.PI * 2;

// Scaling Constants for Canvas
export const CANVAS_SIZE = 500;
const ORIGIN = CANVAS_SIZE / 2;

const RADIUS = CANVAS_SIZE / 2 - 10;

let allData = {};
let loaded = false;
let index = 0;
let qubits = {};
let maxMag = 1;

export function loadQubits(newData, newIndex) {
    loaded = true;
    index = newIndex;
    allData = newData;
    maxMag = newData.maxMag;
    qubits = newData.phis;
}

function drawCircle(ctx, cx, cy, radius, colour, fill=false) {
    ctx.strokeStyle = colour;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, TAU);

    if (fill) {
        ctx.fill();
    } else {
        ctx.stroke();
    }
}

function drawLine(ctx, x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke(); 
}

function drawFrame(ctx, colour) {
    drawCircle(ctx, ORIGIN, ORIGIN, RADIUS, colour);
    ctx.strokeStyle = colour;
    drawLine(ctx, 0, ORIGIN, CANVAS_SIZE, ORIGIN);
    drawLine(ctx, ORIGIN, 0, ORIGIN, CANVAS_SIZE);
}

function plotManyComplex(ctx) {
    function getColour(i) {
        const percentage = i * 360 / Object.keys(qubits[index]).length;
        return HueAngleToRGB(percentage);
    }

    let i = 0;
    for (const num of Object.values(qubits[index])) {
        const colour = getColour(i);
        plotComplex(ctx, num, colour);
        i++;
    }
    
}

function plotComplex(ctx, complexNumber, colour) {
    const angle = -complexNumber.angle();
    const magnitude = complexNumber.magnitude();

    const pointRadius = magnitude * RADIUS / maxMag;
    const pt = rotatePoint(ORIGIN, ORIGIN, ORIGIN + pointRadius, ORIGIN, angle);

    ctx.fillStyle = colour;
    ctx.strokeStyle = colour;
    drawLine(ctx, ORIGIN, ORIGIN, pt.x, pt.y);
    drawCircle(ctx, pt.x, pt.y, 2, colour, true);
}

function rotatePoint(originX, originY, pointX, pointY, angle) {
	const COS = Math.cos(angle);
	const SIN = Math.sin(angle);

	return {x: COS * (pointX - originX) - SIN * (pointY - originY) + originX,
			y: SIN * (pointX - originX) - COS * (pointY - originY) + originY};
}

export function draw(ctx){
  ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE );

  ctx.font = '14pt Arial';
  if (loaded) {
    plotManyComplex(ctx);
    ctx.fillStyle = 'black';
    ctx.fillText(`Fidelity: ${allData.fidelity_series[index].toFixed(3)}`, 20, 20);
    ctx.fillText(`Loss: ${allData.loss_series[index].toFixed(3)}`, 20, 40);
  } else {
    ctx.fillText('Loading. Please stand by.', 20, 20);
  }
  
  drawFrame(ctx, 'black');
};