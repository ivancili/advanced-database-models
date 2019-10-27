// import React from 'react';
// import {Form, Message} from 'semantic-ui-react';
//
// export default class Search extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = {query: '', logical_op: 'and', sql_query: '', search_result: []}
//     }
//
//     handleSubmit = () => {
//         if (this.state.query === '') {
//             alert('Query cannot be empty');
//             return;
//         }
//
//         fetch('http://localhost:5551/search', {
//             method: 'POST',
//             headers: {
//                 'Accept': 'application/json',
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(this.state)
//         })
//             .then((response) => response.json())
//             .then(jsonData => {
//                 console.log(jsonData);
//
//                 this.setState({query: ''});
//                 this.setState({sql_query: jsonData['sql']});
//                 this.setState({search_result: jsonData['rows']});
//             })
//     };
//
//     handleQueryChange = (e, {value}) => this.setState({query: value});
//
//     handleRadioChange = (e, {value}) => this.setState({logical_op: value});
//
//     render() {
//         const {query, logical_op, sql_query, search_result} = this.state;
//
//         const search_elements = search_result.map(r =>
//             <pre
//                 dangerouslySetInnerHTML={{
//                     __html: r[4].toString().concat('\t', r[1], ': ', r[3])
//                 }}
//                 key={r[0]}
//             />
//         );
//
//         return (
//             <div>
//                 <Form onSubmit={this.handleSubmit}>
//                     <Form.Field>
//                         <Form.Input
//                             placeholder='Search query'
//                             name='query'
//                             value={query}
//                             onChange={this.handleQueryChange}
//                         />
//                     </Form.Field>
//
//                     <Form.Group inline>
//                         <label>Logical operator:</label>
//                         <Form.Radio
//                             label='AND'
//                             value='and'
//                             checked={logical_op === 'and'}
//                             onChange={this.handleRadioChange}
//                         />
//                         <Form.Radio
//                             label='OR'
//                             value='or'
//                             checked={logical_op === 'or'}
//                             onChange={this.handleRadioChange}
//                         />
//                     </Form.Group>
//
//                     <Form.Button content='Search'/>
//
//                     <Message>
//                         <Message.Header>SQL query:</Message.Header>
//                         <pre>{sql_query}</pre>
//                     </Message>
//
//                     <Message>
//                         <Message.Header>Results:</Message.Header>
//                         {search_elements}
//                     </Message>
//
//                 </Form>
//             </div>
//         )
//     }
// }
