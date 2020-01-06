import datetime
from typing import Optional

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from utils import get_map_reduce_fns
from utils import get_mongo_client

app = Flask(__name__)


@app.route('/api/v1/comments/<article>')
def _get_comments(
        article: str,
):
    with get_mongo_client() as client:
        data = client.nmbp.comments.find_one(
            {'_id': article},
            {'_id': 0, 'comments': 1}
        )

        return make_response(
            jsonify({
                'article': article,
                'comments': data['comments'] if data else [],
            })
        )


@app.route('/api/v1/comment', methods=['POST'])
def _post_comment():
    article = request.json.get('article')
    comment = request.json.get('comment')

    with get_mongo_client() as client:
        if client.nmbp.comments.find({'_id': article}).count() > 0:
            client.nmbp.comments.update(
                {'_id': article},
                {'$push': {
                    'comments': {
                        'comment': comment,
                        'date': datetime.datetime.now()
                    }
                }}
            )
        else:
            client.nmbp.comments.save({
                '_id': article,
                'comments': [{
                    'comment': comment,
                    'date': datetime.datetime.now()
                }]
            })

        return make_response(
            jsonify({
                'article': article,
                'comment': comment,
            })
        )


@app.route('/api/v1/articles/')
@app.route('/api/v1/articles/<int:number_of_articles>')
def _get_articles(
        number_of_articles: Optional[int] = 10,
):
    with get_mongo_client() as client:
        query = {'date': {'$lt': datetime.datetime.now()}}

        return make_response(
            jsonify(
                list(
                    client.nmbp.news.aggregate([
                        {'$match': query},
                        {'$project': {
                            '_id': 0,
                            'article': {'$toString': '$_id'},
                            'title': 1,
                            'author': 1,
                            'content': 1,
                            'image_url': 1,
                            'date': {
                                '$dateToString': {
                                    'date': '$date'
                                }
                            },
                        }},
                        {'$limit': number_of_articles}
                    ])
                )
            )
        )


@app.route('/api/v1/map_reduce/a')
def _map_reduce_a():
    with get_mongo_client() as client:
        _map_fn, _reduce_fn, _finalize_fn = get_map_reduce_fns('a')

        collection = client.nmbp.comments.map_reduce(
            map=_map_fn,
            reduce=_reduce_fn,
            finalize=_finalize_fn,
            out='map_reduced',
        )

        return make_response(
            jsonify(list(
                collection.find()
            ))
        )


@app.route('/api/v1/map_reduce/b')
def _map_reduce_b():
    with get_mongo_client() as client:
        _map_fn, _reduce_fn, _ = get_map_reduce_fns('b')

        collection = client.nmbp.comments.map_reduce(
            map=_map_fn,
            reduce=_reduce_fn,
            out='map_reduced',
        )

        obj = collection.find_one()
        num_articles = client.nmbp.news.count()
        obj['frequency'] = obj['value'] / num_articles

        return make_response(jsonify(obj))


@app.route('/api/v1/map_reduce/c')
def _map_reduce_c():
    with get_mongo_client() as client:
        _map_fn, _reduce_fn, _finalize_fn = get_map_reduce_fns('c')

        collection = client.nmbp.news.map_reduce(
            map=_map_fn,
            reduce=_reduce_fn,
            finalize=_finalize_fn,
            out='map_reduced',
            limit=500,
        )

        return make_response(
            jsonify(list(
                collection.find()
            ))
        )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
