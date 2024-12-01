import React from "react";
import WeatherDataModel from "../../../models/WeatherDataModel";


const CurrentWeather: React.FC<{weatherData: WeatherDataModel}> = (props) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex justify-between items-center">
        <h2 className="text-gray-600 font-semibold">CURRENT WEATHER</h2>
        <span className="text-gray-500 text-sm">10:07PM</span>
      </div>
      <div className="mt-2 flex">
        <div className="flex-1">
          <div className="flex items-center">
            <img src={props.weatherData.icon} alt="Weather Icon" className="mr-2" />
            <div>
              <span className="text-5xl font-bold">{props.weatherData.temp}°</span>
              <span className="text-2xl text-gray-500">C</span>
            </div>
          </div>
          <div className="text-gray-500">RealFeel® °</div>
          <div className="text-gray-800 font-semibold mt-2">{props.weatherData.condition}</div>
          <a href="#" className="text-blue-500">
            MORE DETAILS &gt;
          </a>
        </div>
        <div className="flex-1 text-right">
          <div className="text-gray-600">Wind</div>
          <div className="text-gray-800 font-semibold">{props.weatherData.wind}</div>
          <div className="text-gray-600 mt-2">Wind Gusts</div>
          <div className="text-gray-800 font-semibold">{props.weatherData.windGusts}</div>
          <div className="text-gray-600 mt-2">Air Quality</div>
          <div className="text-purple-600 font-semibold">{props.weatherData.airQuality}</div>
        </div>
      </div>
    </div>
  );
};

export default CurrentWeather;
