from flask import Flask, request, render_template, json
import flask_cors

import api

app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('base.html')


@app.route('/multivector', methods=['POST'])
def get_multivector():
    recv = request.get_json(force=True)

    coords = []
    for i in ('r0', 'i0', 'r1', 'i1'):
        coords.append(float(recv[i]))

    output = {}
    output['img'] = api.show_multivector(coords).decode()

    return json.dumps(output)


@app.route('/radial', methods=['POST'])
def get_radial():
    recv = request.get_json(force=True)

    coords = recv['radialX'], recv['radialY'], 1

    output = {}
    output['img'] = api.show_radial(coords).decode()

    return json.dumps(output)


if __name__ == '__main__':
    app.run()
