import React from "react";


export const TmrWeatherTab: React.FC<{
    title: string;
    forecast: string;
}> = (props) => {
    return (
        <div className="bg-white rounded-lg shadow-md p-4">
            <h2 className="text-gray-600 font-semibold">{props.title}</h2>
            <div className="mt-2 text-gray-800">{props.forecast}</div>
        </div>
    );
};
