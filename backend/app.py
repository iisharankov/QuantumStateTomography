from flask import Flask, request, render_template, json
import flask_cors
import traceback

import api
import qml

app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('base.html')


@app.route('/multivector', methods=['POST'])
def get_multivector():
    # Deprecated
    recv = request.get_json(force=True)

    coords = []
    for i in ('r0', 'i0', 'r1', 'i1'):
        coords.append(float(recv[i]))

    output = {}
    output['img'] = api.show_multivector(coords).decode()

    return json.dumps(output)


@app.route('/radial', methods=['POST'])
def get_radial():
    # Deprecated
    recv = request.get_json(force=True)

    coords = recv['radialX'], recv['radialY'], 1

    output = {}
    output['img'] = api.show_radial(coords).decode()

    return json.dumps(output)


@app.route('/qml', methods=['POST'])
def get_qml():
    # Quantum machine learning endpoint
    recv = request.get_json(force=True)

    try:
        output = qml.show_phis(recv)
    except:
        print('get_qml error')
        traceback.print_exc()
        return json.dumps('Error')
    else:
        print('get_qml success')
        return json.dumps(output)


if __name__ == '__main__':
    app.run()
