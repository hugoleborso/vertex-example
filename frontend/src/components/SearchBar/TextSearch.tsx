import React, { useState, ChangeEvent, FormEvent } from 'react';
import { TextInput, Button } from 'flowbite-react';
import { Loader } from '../Loader/Loader';

interface TextSearchProps {
    onSearch: (results: any) => void;
}

export const TextSearch: React.FC<TextSearchProps> = ({ onSearch }) => {
    const [searchQuery, setSearchQuery] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleSearch = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setIsLoading(true);
        const response = await fetch('http://0.0.0.0:8000/search-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: searchQuery }),
        });
        const results = await response.json();
        onSearch(results);
        setIsLoading(false);
    };

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
    };

    return (
        <form onSubmit={handleSearch} className="flex flex-col items-center">
            <h2>Text search</h2>
            <div className='flex flex-row space-x-4'>
                <TextInput
                    id="searchInput"
                    type="text"
                    value={searchQuery}
                    onChange={handleInputChange}
                    placeholder="Search..."
                    className="h-10 w-400"
                />
                <Button type="submit" color="success" className="h-10">
                    {isLoading ? <Loader/> : 'Search'}
                </Button>
            </div>
        </form>
    );
};