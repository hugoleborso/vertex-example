import React from 'react';
import {ImageResult} from '../ImageResult/ImageResult';

interface ResultsSectionProps {
    results: { imageUrl: string; imageName: string; percentage: number }[];
}

export const ResultsSection: React.FC<ResultsSectionProps> = ({ results }) => {
    return (
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '20px' }}>
            {results.map((result, index) => (
                <ImageResult key={index} imageUrl={result.imageUrl} imageName={result.imageName} percentage={result.percentage} />
            ))}
        </div>
    );
};

