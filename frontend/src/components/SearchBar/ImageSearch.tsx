import React, { useState, ChangeEvent } from 'react';
import { FileInput, Button } from 'flowbite-react';
import { Loader } from '../Loader/Loader';

interface ImageSearchProps {
    onSearch: (results: any) => void;
}

export const ImageSearch: React.FC<ImageSearchProps> = ({ onSearch }) => {
    const [isImageLoading, setIsImageLoading] = useState<boolean>(false);
    const [selectedImage, setSelectedImage] = useState<File | null>(null);

    const handleImageSearch = async () => {
        if (!selectedImage) return;
        setIsImageLoading(true);
        const reader = new FileReader();
        reader.onloadend = async () => {
            const base64data = reader.result;
            const response = await fetch('http://0.0.0.0:8000/search-image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_bytes: base64data }),
            });
            const results = await response.json();
            onSearch(results);
            setIsImageLoading(false);
        };
        reader.readAsDataURL(selectedImage);
    };

    const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
        setSelectedImage(event.target.files ? event.target.files[0] : null);
    };

    return (
        <div className="flex flex-col items-center">
            <h2>Image search</h2>
            <div className='flex flex-row space-x-4'>
                
                <FileInput 
                    id="file-upload" 
                    // helperText="SVG, PNG, JPG, or GIF (MAX. 800x400px)." 
                    onChange={handleImageChange}
                    className="h-10"
                />

                {selectedImage && <img src={URL.createObjectURL(selectedImage)} alt="Preview" className="
                w-10 rounded-md h-10" />}
                <Button onClick={handleImageSearch} color="success" className="h-10">
                    {isImageLoading ? <Loader/> : 'Search Image'}
                </Button>
            </div>
        </div>
    );
};