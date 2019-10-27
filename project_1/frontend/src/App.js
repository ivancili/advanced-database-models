import React from 'react';
import {Tab} from "semantic-ui-react";
import Add from './components/Add';
import Search from './components/Search';
import Analysis from './components/Analysis';

export default class App extends React.Component {

    render() {
        const panes = [
            {menuItem: 'Add', render: () => <Tab.Pane><Add/></Tab.Pane>},
            {menuItem: 'Search', render: () => <Tab.Pane><Search/></Tab.Pane>},
            {menuItem: 'Analysis', render: () => <Tab.Pane><Analysis/></Tab.Pane>},
        ];

        return (
            <div className="App">
                <Tab panes={panes}/>
            </div>
        );
    }
}
