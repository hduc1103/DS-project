import React from 'react';
import WeatherDataModel from '../../models/WeatherDataModel';
import { WeatherRow } from './components/WeatherRow';

const WeatherForecast: React.FC<{weatherDataArray: WeatherDataModel[]}> = (props) => {
    return (
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="p-4 border-b border-gray-200">
                <h1 className="text-xl font-bold">10-DAY WEATHER FORECAST</h1>
            </div>
            {props.weatherDataArray.map((data, index) => (
                <WeatherRow weatherData={data} key={index} />
            ))}
        </div>
    );
};

export default WeatherForecast;