import os
from typing import Tuple

from pymongo import MongoClient

__SECRET_PW = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
__SECRET_UNAME = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

__MAP_REDUCE_A = (
    """
    function() {
        var num_comments = this.comments.length;
        emit(num_comments, {num_comments: num_comments, num_coresponding_articles: 1});
    };
    """,

    """
    function(key, values) {
        ret = {num_comments: key, num_coresponding_articles: 0};
        values.forEach(function(elem) {
            ret.num_coresponding_articles += elem.num_coresponding_articles;
        });
        return ret;
    };
    """,

    """
    function (key, reducedVal) {
        return reducedVal;
    };
    """,
)

__MAP_REDUCE_B = (
    """
    function() {
        emit('num_commented', 1);
    };
    """,

    """
    function(key, values) {
        var total = 0;
        values.forEach(function(elem) {
            total += elem;
        });
        return total;
    };
    """,

    """
    function (key, reducedVal) {
        return {commented_articles: reducedVal};
    };
    """,
)

__MAP_REDUCE_C = (
    """
    function() {
        var author = this.author;
        author = author.trim();
        author = author.replace('<strong>', '');
        author = author.replace('</strong>', '');
        author = author.replace('<sub>', '');
        author = author.replace('</sub>', '');
        
        var words = this.content.split(/[ ,]+/).filter(Boolean);
        
        words.forEach(function(word) { 
            emit(author, {[word]: 1});
        });
    };
    """,

    """
    function(key, values) {        
        var counts = {};
        
        values.forEach(function(word_dict) {
            Object.keys(word_dict).forEach(function(key) {
                counts[key] = (counts[key] || 0) + word_dict[key];
            });
        });
        
        return counts;
    };
    """,

    """
    function (key, reducedVal) {
        var arr = [];
        
        Object.keys(reducedVal).forEach(function(key){
            arr.push([reducedVal[key], key]);
        });
                
        arr.sort((a, b) => {
            return b[0] - a[0];
        });
        
        return arr.slice(0, 10);
    };
    """,
)


def get_mongo_client() -> MongoClient:
    return MongoClient(
        host=f'mongodb://{__SECRET_UNAME}:{__SECRET_PW}@db',
        connect=False,
    )


def get_map_reduce_fns(option: str) -> Tuple[str, str, str]:
    return {
        'a': __MAP_REDUCE_A,
        'b': __MAP_REDUCE_B,
        'c': __MAP_REDUCE_C,
    }[option.lower()]
