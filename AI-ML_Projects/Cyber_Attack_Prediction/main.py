from flask import Flask, render_template, make_response, jsonify, request
import pandas
from joblib import dump, load
app = Flask(__name__)

df = pandas.read_csv('dataset.csv')
cyber_data = pandas.read_csv('cyber.csv')


@app.route('/api', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        name = request.get_json()['name']
        row = df[df['State/UT'].str.contains(name, case=False)]
        full_data = row.to_dict(orient='records')[0]
        graph_row = row.drop(['Total Crimes', 'State/UT'], axis=1)
        graph_data = graph_row.to_dict(orient='records')[0]

        graph_arr = [['Year', 'Cases']]
        for key, val in graph_data.items():
            graph_arr.append([key, val])

        return make_response(jsonify({
            'name': full_data['State/UT'],
            'data': full_data,
            'graph': graph_arr
        }))
    else:
        return make_response(jsonify({'error': 'UnAuthorised!'}))


@app.route('/')
def index():
    return render_template('index.html')


def find_max_key(value: int, all_years_predictions: dict) -> str:
    for key, val in all_years_predictions.items():
        if val == value:
            return key


@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        state_info = request.get_json()['state_info']
        state = state_info['state']
        state_info.pop('state')
        sample = [int(val) for key, val in state_info.items()]
        all_states = list(set(cyber_data['State'].to_list()))
        all_states.sort()
        state_df = cyber_data[cyber_data['State'] == state]
        years_known = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
        years_data_known = state_df['Cases Reported'].to_list()

        years_display = [x for x in years_known]
        years_display.append(int(state_info['year']))

        state_data = state_df.to_dict(orient='list')
        rm_keys = ['Unique Code', 'State']
        for key in rm_keys:
            state_data.pop(key)
        path = f'models/{state}.joblib'
        loaded_model = load(path)
        # sample_input = [[2022, 90000000, 60000000, 57000000, 59000000]]
        result = loaded_model.predict([sample])

        X = state_df.drop(['Unique Code', 'State', 'Cases Reported'], axis=1)
        years_data_display = list(loaded_model.predict(X.values))
        years_data_display.append(result[0])

        years_data_display = [int(x) for x in years_data_display]

        # print(years_data_display)

        all_years_predictions = {}
        all_predictions = []
        for i in all_states:
            path = f'models/{i}.joblib'
            model = load(path)
            value = int(model.predict([sample])[0])
            all_years_predictions[i] = value
            all_predictions.append(value)

        max_val = max(all_predictions)

        return make_response(jsonify(
            {
                'state_data': state_data,
                'result': result[0],
                'years_known': years_known,
                'years_data_known': years_data_known,
                'years_display': years_display,
                'years_data_display': years_data_display,
                'all_years_predictions': all_years_predictions,
                'max_predictions': find_max_key(max_val, all_years_predictions)
            }
        ))
    else:
        return render_template('predictions.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
