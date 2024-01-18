import React from 'react';

import 'tailwindcss/tailwind.css';
import { TextSearch } from './TextSearch';
import { ImageSearch } from './ImageSearch';


interface SearchBarProps {
    onSearch: (results: any) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    return(
        <div className='flex flex-row space-x-14'>
            <TextSearch onSearch={onSearch}/>
            <ImageSearch onSearch={onSearch}/>
        </div>
    )
};

