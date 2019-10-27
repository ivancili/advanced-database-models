import React from 'react';
import {Form} from 'semantic-ui-react';

export default class Add extends React.Component {

    constructor(props) {
        super(props);
        this.state = {movie: '', category: '', summary: '', description: ''}
    }

    handleSubmit = () => {
        fetch('http://localhost:5551/add', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.state)
            }
        )
            .then(response => response.json())
            .then(jsonData => {
                console.log(jsonData);

                this.clearState();
            })
    };

    handleChange = (e, {name, value}) => this.setState({[name]: value});

    clearState = () => this.setState({movie: '', category: '', summary: '', description: ''});

    render() {
        const {movie, category, summary, description} = this.state;

        return (
            <Form style={{width: '40%'}} onSubmit={this.handleSubmit}>

                <Form.Field>
                    <label>Title</label>
                    <Form.Input
                        placeholder='Movie title'
                        onChange={this.handleChange}
                        name='movie'
                        value={movie}
                    />
                </Form.Field>

                <Form.Field>
                    <label>Categories</label>
                    <Form.Input
                        placeholder='Movie categories'
                        onChange={this.handleChange}
                        name='category'
                        value={category}
                    />
                </Form.Field>

                <Form.Field>
                    <label>Summary</label>
                    <Form.Input
                        placeholder='Movie summary'
                        onChange={this.handleChange}
                        style={{height: '150px'}}
                        name='summary'
                        value={summary}
                    />
                </Form.Field>

                <Form.Field>
                    <label>Description</label>
                    <Form.Input
                        placeholder='Movie description'
                        onChange={this.handleChange}
                        style={{height: '150px'}}
                        name='description'
                        value={description}
                    />
                </Form.Field>

                <Form.Button content='Submit'/>

            </Form>
        )
    }
}
