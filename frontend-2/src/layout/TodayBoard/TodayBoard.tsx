import React from "react";
import UpcomingWeatherTab from "./components/UpcomingWeatherTab";
import CurrentWeather from "./components/CurrentWeather";
import { TmrWeatherTab } from "./components/TmrWeatherTab";
import WeatherDataModel from "../../models/WeatherDataModel";

export const TodayBoard: React.FC<{todayWeatherData: WeatherDataModel, tmrWeatherData: WeatherDataModel}> = (props) => {
  return (
    <div className="max-w-md mx-auto mt-10">
      <UpcomingWeatherTab
        // title="TONIGHT'S WEATHER"
        // date="SAT, NOV 30"
        // icon="fas fa-moon"
        // condition="Clear"
        // temperature="Lo: 16°"
        // tomorrowCondition="Partly sunny"
        // tomorrowTemperature="Hi: 27°"
        weatherData={props.todayWeatherData}
        title="TONIGHT'S WEATHER"
        tmrWeatherData={props.tmrWeatherData}
      />
      <CurrentWeather
        // temp="20"
        // realFeel="19"
        // condition="Mostly clear"
        // wind="E 4 km/h"
        // windGusts="11 km/h"
        // airQuality="Very Unhealthy"
        // icon="https://placehold.co/50x50"
        weatherData={props.todayWeatherData}
      />
      <TmrWeatherTab
        title="LOOKING AHEAD"
        forecast="Expect rainy weather Wednesday morning through late Wednesday night"
      />
    </div>
  );
};