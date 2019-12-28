import React from 'react';
import ArticleList from './components/ArticleList';

function App() {
    return (
        <div className='App'>
            <ArticleList num_articles={10}/>
        </div>
    );
}

export default App;
