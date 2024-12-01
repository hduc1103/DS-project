import React from "react";
import WeatherDataModel from "../../../models/WeatherDataModel";


const WeatherCard: React.FC<{weatherData: WeatherDataModel, title: string, tmrWeatherData: WeatherDataModel}> = (props) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex justify-between items-center">
        <h2 className="text-gray-600 font-semibold">{props.title}</h2>
        <span className="text-gray-500 text-sm">{props.weatherData.date}</span>
      </div>
      <div className="mt-2">
        <div className="flex items-center">
          <i className={`${props.weatherData.icon} text-gray-600 mr-2`}></i>
          <span className="text-gray-800">
            {props.weatherData.condition} <span className="font-bold">{props.weatherData.temp}</span>
          </span>
        </div>
        <div className="flex items-center mt-2">
          <i className="fas fa-sun text-yellow-500 mr-2"></i>
          <span className="text-gray-800">
            Tomorrow: {props.tmrWeatherData.condition} <span className="font-bold">{props.tmrWeatherData.temp}</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
