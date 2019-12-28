import React from 'react';
import {Divider, Form, Item, List} from 'semantic-ui-react';

class Article extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            comments: [],
            comment: ''
        }
    }

    recordComment = (e, {name, value}) => {
        this.setState({[name]: value});
    };

    handleSubmit = () => {
        const {comment} = this.state;
        const {article} = this.props.data;
        this.postComments(article, comment);
        this.setState({comment: ''});
    };

    postComments = (article, comment) => {
        fetch(`/api/v1/comment`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                article: article,
                comment: comment
            })
        }).finally(() => this.fetchComments(article));
    };

    fetchComments = (article) => {
        fetch(`/api/v1/comments/${article}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(jsonData => this.setState({
                comments: jsonData.comments
            }))
    };

    componentDidMount() {
        const {article} = this.props.data;
        this.fetchComments(article);
    }

    render() {
        const {comments, comment} = this.state;
        const {author, title, content, image_url} = this.props.data;

        const comment_list = comments.map((element) =>
            <List.Item style={{paddingBottom: '10px'}}>
                <List.Content>{element.date}</List.Content>
                <List.Icon name='comment'/>
                <List.Content>{element.comment}</List.Content>
            </List.Item>
        );

        return (
            <Item style={{paddingTop: '2%'}}>

                <Item.Image size='medium' src={image_url}/>
                <Item.Content>

                    <Item.Meta content={author}/>
                    <Item.Header as='a' content={title}/>
                    <Item.Description content={content}/>

                    <Divider/>

                    <Item.Header as='a' content='Comments'/>
                    <List>
                        {comment_list}
                    </List>

                    <Form widths='equal' onSubmit={this.handleSubmit}>
                        <Form.Group>
                            <Form.Input
                                name='comment'
                                value={comment}
                                placeholder='Comment here...'
                                onChange={this.recordComment}
                            />
                            <Form.Button content='Send'/>
                        </Form.Group>
                    </Form>

                </Item.Content>

            </Item>
        )
    }

}

export default Article;