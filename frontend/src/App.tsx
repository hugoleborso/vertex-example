import React, { useState } from 'react';
import {SearchBar} from './components/SearchBar/SearchBar';
import {ResultsSection} from './components/ResultSection/ResultSection';

const App: React.FC = () => {
    const [results, setResults] = useState([]);

    const handleSearch = (newResults: any) => {
        setResults(newResults);
    };

    return (
        <div className="flex flex-col items-center p-4">
            <img src="fse-logo.png" alt="Logo" className="w-36 mb-4" />
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Food Search Engine</h1>
            <SearchBar onSearch={handleSearch} />
            <ResultsSection results={results} />
        </div>
    );
};

export default App;