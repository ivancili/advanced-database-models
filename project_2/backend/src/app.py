import datetime
import random
from typing import Optional

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

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
    article = request.args.get('article')
    comment = request.args.get('comment')

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
    def _add_fake_image(entry):
        entry['image_url'] = f'https://picsum.photos/id/{random.randint(1, 1000)}/200/200'
        return entry

    with get_mongo_client() as client:
        query = {'date': {'$lt': datetime.datetime.now()}}

        return make_response(
            jsonify(
                list(map(
                    _add_fake_image,
                    client.nmbp.news.aggregate([
                        {'$match': query},
                        {'$project': {
                            '_id': 0,
                            'article': {'$toString': '$_id'},
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
                ))
            )
        )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
