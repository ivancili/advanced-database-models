import React from 'react';
import Article from "./Article";
import {List} from 'semantic-ui-react';

class ArticleList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {articles: []}
    }

    fetchArticles = (num_articles) => {
        fetch(`/api/v1/articles/${num_articles}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })
            .then((response) => response.json())
            .then(articles => {
                this.setState({articles: articles})
            })
    };

    componentDidMount() {
        this.fetchArticles(this.props.num_articles);
    }

    render() {
        const articleList = this.state.articles.map((article, i) =>
            <List.Item>
                <Article key={i} data={article}/>
            </List.Item>
        );

        return (
            <List divided verticalAlign='middle'>
                {articleList}
            </List>
        )
    }

}

export default ArticleList;