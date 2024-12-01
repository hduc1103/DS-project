import React from 'react';
import WeatherDataModel from '../../../models/WeatherDataModel';

export const WeatherRow: React.FC<{weatherData: WeatherDataModel}> = (props) => {
    return (
        <div className="flex justify-between items-center p-4 border-b border-gray-200">
            <div className="flex items-center w-1/6">
                <div className="text-left">
                    <div className="font-bold">{props.weatherData.day}</div>
                    <div className="text-gray-500">{props.weatherData.date}</div>
                </div>
                <div className="ml-auto text-2xl">
                    <i className={props.weatherData.icon}></i>
                </div>
            </div>
            <div className="text-center w-1/6">
                <div className="text-2xl font-bold">{props.weatherData.temp}</div>
            </div>
            <div className="text-left w-3/6">
                <div className="text-gray-500">{props.weatherData.condition}</div>
                {props.weatherData.nightCondition && <div className="text-gray-500">{props.weatherData.nightCondition}</div>}
                {props.weatherData.subCondition && <div className="text-gray-500">{props.weatherData.subCondition}</div>}
            </div>
            <div className="text-right w-1/6">
                <div className="text-gray-500"><i className="fas fa-tint"></i> {props.weatherData.precip}</div>
            </div>
        </div>
    );
};