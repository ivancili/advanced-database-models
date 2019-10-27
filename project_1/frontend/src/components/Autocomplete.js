import React, {Component} from 'react'
import {Search} from 'semantic-ui-react'

const initialState = {isLoading: false, results: []};

export default class AutocompleteSearch extends Component {

    constructor(props) {
        super(props);
        this.state = initialState;
    }

    handleSearchChange = (e, {value}) => {
        this.setState({isLoading: true});
        this.props.onChangeOrSelect({title: value});

        setTimeout(() => {
            if (this.props.value.length === 0) {
                this.setState(initialState);
            }

            this.props.onSearch(value).then(response =>
                this.setState({
                    isLoading: false,
                    results: response,
                })
            );
        }, 300)
    };

    handleResultSelect = (e, {result}) => {
        this.props.onChangeOrSelect(result);
    };

    render() {
        const {isLoading, results} = this.state;

        return (
            <Search
                loading={isLoading}
                onResultSelect={this.handleResultSelect}
                onSearchChange={this.handleSearchChange}
                results={results}
                value={this.props.value}
                resultRenderer={({title}) => <p>{title}</p>}
            />
        )
    }
}