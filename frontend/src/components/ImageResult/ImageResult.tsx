import React, { useState } from 'react';


interface ImageResultProps {
    imageUrl: string;
    imageName: string;
    percentage: number;
}

export const ImageResult: React.FC<ImageResultProps> = ({ imageUrl, imageName, percentage }) => {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <div className="relative w-48 h-48 m-2 rounded" onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>
            <img src={`http://0.0.0.0:8000/${imageUrl}`} alt={imageName} className="w-full h-full object-cover rounded" />
            <div className={`rounded absolute top-0 left-0 w-full h-full flex flex-col justify-center items-center bg-black bg-opacity-50 text-white ${isHovered ? 'opacity-100' : 'opacity-0'} transition-opacity duration-300 ease-in-out text-center`}>
                <h3 className="w-36 break-words text-gray-400">{imageName}</h3>
                <p>{percentage.toFixed(2)}% match</p>
            </div>
        </div>
    );
};