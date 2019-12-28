import datetime
import json
from typing import Optional

from bson.json_util import dumps
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

from utils import get_mongo_client

app = Flask(__name__)


@app.route('/api/v1/comments')
def _get_comments():
    article = request.args.get('article')

    with get_mongo_client() as client:
        data = json.loads(dumps(
            client.nmbp.comments.find_one({'_id': article})
        ))

        return make_response(
            jsonify({'comments': data['comments'] if data else []})
        )


@app.route('/api/v1/comment', methods=['POST'])
def _post_comment():
    article = request.args.get('article')
    comment = request.args.get('comment')

    with get_mongo_client() as client:
        if client.nmbp.comments.find({'_id': article}).count() > 0:
            client.nmbp.comments.update(
                {'_id': article},
                {'$push': {'comments': comment}}
            )
        else:
            client.nmbp.comments.save(
                {'_id': article, 'comments': [comment]}
            )

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
                            '_id': {'$toString': '$_id'},
                            'title': 1,
                            'author': 1,
                            'content': 1,
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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
