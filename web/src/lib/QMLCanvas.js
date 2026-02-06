import HueAngleToRGB from './HueAngleToRGB';


const TAU = Math.PI * 2;

// Scaling Constants for Canvas
export const CANVAS_SIZE = 500;
const ORIGIN = CANVAS_SIZE / 2;

const RADIUS = CANVAS_SIZE / 2 - 10;

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

function plotManyComplexTrail(ctx, qubits, index, maxMag) {
    function getColour(i, length) {
        const percentage = i * 360 / length;
        return HueAngleToRGB(percentage);
    }

    const currentQubits = Object.values(qubits[index]);
    let i = 0;
    for (const num of currentQubits) {
        const colour = getColour(i, currentQubits.length);
        plotComplexSpan(ctx, num, colour, maxMag);
        i++;
    }

}

function plotManyComplexSpan(ctx, qubits, index, maxMag) {
    function getColour(i, length) {
        const percentage = i * 360 / length;
        return HueAngleToRGB(percentage);
    }

    const MAX = 4;
    for (let radius = MAX; radius > 0; radius--) {
        function drawPlot(tempIndex) {
            if (tempIndex >= 0 && tempIndex < qubits.length) {
                const currentQubits = Object.values(qubits[tempIndex]);
                let i = 0;
                for (const num of currentQubits) {
                    const colour = getColour(i, currentQubits.length);
                    plotComplexPoint(ctx, num, colour, radius, maxMag);
                    i++;
                }
            }
        }

        const delta = MAX - radius;
        drawPlot(index + delta);
        drawPlot(index - delta);
    }
}

function getComplexPoint(complexNumber, maxMag) {
    const angle = -complexNumber.angle();
    const magnitude = complexNumber.magnitude();

    const pointRadius = magnitude * RADIUS / maxMag;
    return rotatePoint(ORIGIN, ORIGIN, ORIGIN + pointRadius, ORIGIN, angle);
}

function plotComplexPoint(ctx, complexNumber, colour, radius, maxMag) {
    const pt = getComplexPoint(complexNumber, maxMag);

    ctx.fillStyle = colour;
    ctx.strokeStyle = colour;
    drawCircle(ctx, pt.x, pt.y, radius, colour, true);
}

function plotComplexSpan(ctx, complexNumber, colour, maxMag) {
    const pt = getComplexPoint(complexNumber, maxMag);

    ctx.fillStyle = colour;
    ctx.strokeStyle = colour;
    drawLine(ctx, ORIGIN, ORIGIN, pt.x, pt.y);
    drawCircle(ctx, pt.x, pt.y, 4, colour, true);
}

function rotatePoint(originX, originY, pointX, pointY, angle) {
	const COS = Math.cos(angle);
	const SIN = Math.sin(angle);

	return {x: COS * (pointX - originX) - SIN * (pointY - originY) + originX,
			y: SIN * (pointX - originX) - COS * (pointY - originY) + originY};
}

export function draw(ctx, canvasState) {
  ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

  ctx.font = '14pt Arial';
  if (!canvasState) {
    ctx.fillStyle = 'white';
    ctx.fillText('Loading. Please stand by.', 20, 20);
    drawFrame(ctx, 'white');
    return;
  }

  const { allData, index, visual } = canvasState;
  const qubits = allData.phis;
  const maxMag = allData.maxMag;

  if (visual === 'Line') {
    plotManyComplexTrail(ctx, qubits, index, maxMag);
  } else {
    plotManyComplexSpan(ctx, qubits, index, maxMag);
  }

  ctx.fillStyle = 'white';
  ctx.fillText(`Fidelity: ${allData.fidelity_series[index].toFixed(3)}`, 20, 20);
  ctx.fillText(`Loss: ${allData.loss_series[index].toFixed(3)}`, 20, 40);

  drawFrame(ctx, 'white');
}