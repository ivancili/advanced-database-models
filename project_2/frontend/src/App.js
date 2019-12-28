import React from 'react';
import ArticleList from './components/ArticleList';
import {Header} from "semantic-ui-react";

class App extends React.Component {

    render() {
        return (
            <div className='App'>
                <Header
                    dividing
                    size='huge'
                    content='News portal'
                    style={{textAlign: 'center'}}
                />
                <ArticleList num_articles={10}/>
            </div>
        );
    }

}

export default App;
