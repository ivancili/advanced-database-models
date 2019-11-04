import argparse
import datetime

from flask import Flask
from flask import make_response
from flask import request
from utils import build_analysis_query
from utils import build_search_query
from utils import get_database_ref

app = Flask(__name__)

database_cursor = None
database_connection = None


@app.route('/api/v1/add', methods=['POST'])
def add():
    data = request.json

    try:
        database_cursor.execute(
            "INSERT INTO movie VALUES (%s, %s, %s, %s)",
            (data.get('movie'), data.get('category'), data.get('summary'), data.get('description'))
        )
        database_connection.commit()
    except:
        return make_response({'status_text': 'fail'}, 400)

    return make_response({'status_text': 'success'}, 200)


@app.route('/api/v1/search', methods=['POST'])
def search():
    query = request.json.get('query')
    logical_op = request.json.get('logical_op')

    try:
        database_cursor.execute(
            "INSERT INTO query_logging VALUES (%s, %s)",
            (query, str(datetime.datetime.now()))
        )
        database_connection.commit()
    except:
        return make_response({'status_text': 'insert fail'}, 400)

    try:
        search_query = build_search_query(query, logical_op)

        database_cursor.execute(search_query)
        rows = database_cursor.fetchall()
    except:
        return make_response({'status_text': 'search fail'}, 400)

    return make_response({'sql': search_query, 'rows': rows, 'status_text': 'success'}, 200)


@app.route('/api/v1/search_similar', methods=['POST'])
def search_similar():
    query = request.json.get('partial_query')
    query = query.split(' ')[-1]

    try:
        search_query = f'''
        SELECT
            token 
        FROM tokens
        WHERE similarity(token, '{query}') > 0.05
        ORDER BY similarity(token, '{query}') DESC
        LIMIT 5;
        '''

        database_cursor.execute(search_query)
        rows = database_cursor.fetchall()
    except:
        return make_response({'status_text': 'fail'}, 400)

    return make_response(
        {
            'similar': [{'title': desc[0]} for desc in rows],
            'status_text': 'success'
        }, 200
    )


@app.route('/api/v1/analyse', methods=['POST'])
def analyse():
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    granulation = request.json.get('granulation')

    try:
        analysis_query = build_analysis_query(start_date, end_date, granulation)

        database_cursor.execute(analysis_query)
        rows = database_cursor.fetchall()
        col_names = [desc[0] for desc in database_cursor.description]
    except:
        return make_response({'status_text': 'fail'}, 400)

    return make_response({'status_text': 'success', 'rows': rows or [], 'header': col_names}, 200)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--port', required=False, type=int, default=5000)
    argparser.add_argument('--debug', required=False, action='store_true')
    args = argparser.parse_args()

    database_connection, database_cursor = get_database_ref()
    app.run(
        host='0.0.0.0',
        port=args.port,
        debug=args.debug,
    )
    database_cursor.close()
