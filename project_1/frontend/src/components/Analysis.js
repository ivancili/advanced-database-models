import React from 'react';
import {Form, Table} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

export default class Analysis extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            startDate: new Date(),
            endDate: new Date(),
            granulation: 'hours',
            search_result: [],
            search_header: []
        }
    }

    handleSubmit = () => {
        fetch('/api/v1/analyse', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.state)
        })
            .then((response) => response.json())
            .then(jsonData => {
                console.log(jsonData);
                this.setState({search_result: jsonData['rows'], search_header: jsonData['header']})
            });
    };

    render() {
        const {startDate, endDate, granulation, search_result, search_header} = this.state;

        const search_result_headers = (
            <Table.Row>
                {search_header.map(column => <Table.HeaderCell>{column}</Table.HeaderCell>)}
            </Table.Row>
        );
        const search_result_list = search_result.map(result =>
            <Table.Row>
                {result.map(column => <Table.Cell>{column}</Table.Cell>)}
            </Table.Row>
        );

        return (
            <Form onSubmit={this.handleSubmit}>

                <Form.Group inline>
                    <label>From: </label>
                    <DatePicker
                        showPopperArrow={false}
                        selected={startDate}
                        showTimeSelect
                        dateFormat='yyyy-MM-dd h:mm:ss'
                        onChange={date => this.setState({startDate: date})}
                    />
                </Form.Group>

                <Form.Group inline>
                    <label>Until: </label>
                    <DatePicker
                        showPopperArrow={false}
                        selected={endDate}
                        showTimeSelect
                        dateFormat='yyyy-MM-dd h:mm:ss'
                        onChange={date => this.setState({endDate: date})}
                    />
                </Form.Group>

                <Form.Group inline>
                    <label>Granulation:</label>
                    <Form.Radio
                        label='hours'
                        value='hours'
                        checked={granulation === 'hours'}
                        onChange={(e, {value}) => this.setState({granulation: value})}
                    />
                    <Form.Radio
                        label='days'
                        value='days'
                        checked={granulation === 'days'}
                        onChange={(e, {value}) => this.setState({granulation: value})}
                    />
                </Form.Group>

                <Form.Button content='Submit'/>

                <Table basic style={{fontSize: 11}}>
                    <Table.Header>
                        {search_result_headers}
                    </Table.Header>

                    <Table.Body>
                        {search_result_list}
                    </Table.Body>
                </Table>

            </Form>
        )
    }
};
