import React from "react";
import { TodayBoard } from './layout/TodayBoard/TodayBoard';
import ForecastBoard from './layout/ForecastBoard/ForecastBoard';
import WeatherDataModel from "./models/WeatherDataModel";

const weatherDataSamples = [
  new WeatherDataModel("TONIGHT", "11/30", "16°", "Clear", "Partly cloudy", "", "fas fa-moon", "2%", "E 4 km/h", "11 km/h", "Very Unhealthy"),
  new WeatherDataModel("SUN", "12/1", "27° 20°", "Partly sunny", "Night: Partly cloudy", "", "fas fa-cloud-sun", "1%", "E 5 km/h", "10 km/h", "Unhealthy"),
  new WeatherDataModel("MON", "12/2", "26° 21°", "A little afternoon rain", "Cloudy", "Cloudy", "fas fa-cloud-showers-heavy", "55%", "E 6 km/h", "12 km/h", "Moderate"),
  new WeatherDataModel("TUE", "12/3", "27° 21°", "Some sun, then clouds", "Cloudy", "Cloudy", "fas fa-cloud-sun", "5%", "SE 3 km/h", "9 km/h", "Good"),
  new WeatherDataModel("WED", "12/4", "26° 21°", "A couple of afternoon showers", "Periods of rain", "", "fas fa-cloud-showers-heavy", "72%", "S 7 km/h", "15 km/h", "Unhealthy for Sensitive Groups"),
  new WeatherDataModel("THU", "12/5", "26° 18°", "Clouds with afternoon rain", "Cloudy with occasional rain", "Cloudy", "fas fa-cloud-showers-heavy", "70%", "SW 8 km/h", "14 km/h", "Moderate"),
  new WeatherDataModel("FRI", "12/6", "21° 14°", "A morning shower; not as warm", "Cloudy", "Cloudy", "fas fa-cloud-showers-heavy", "43%", "W 5 km/h", "11 km/h", "Good"),
  new WeatherDataModel("SAT", "12/7", "20° 12°", "Remaining cloudy", "Cloudy", "", "fas fa-cloud", "25%", "WNW 4 km/h", "8 km/h", "Good"),
  new WeatherDataModel("SUN", "12/8", "24° 19°", "Sunny", "Clear", "Clear", "fas fa-sun", "0%", "W 3 km/h", "5 km/h", "Good"),
  new WeatherDataModel("MON", "12/9", "23° 18°", "Partly cloudy", "Clear", "Clear", "fas fa-cloud-sun", "5%", "ESE 6 km/h", "10 km/h", "Good"),
  new WeatherDataModel("TUE", "12/10", "25° 20°", "Mostly sunny", "Clear", "", "fas fa-sun", "0%", "SE 7 km/h", "12 km/h", "Good"),
  new WeatherDataModel("WED", "12/11", "24° 19°", "Cloudy", "Partly cloudy", "", "fas fa-cloud", "10%", "SW 4 km/h", "8 km/h", "Moderate"),
  new WeatherDataModel("THU", "12/12", "22° 17°", "Showers", "Rainy", "Periods of rain", "fas fa-cloud-showers-heavy", "80%", "S 6 km/h", "13 km/h", "Unhealthy for Sensitive Groups"),
  new WeatherDataModel("FRI", "12/13", "20° 15°", "Rainy", "Cloudy with rain", "", "fas fa-cloud-showers-heavy", "95%", "SE 5 km/h", "14 km/h", "Unhealthy"),
];
const App: React.FC = () => {
  return (
      <div className="bg-gray-100 min-h-screen flex">
          <div className="w-2/5 p-4">
              <TodayBoard todayWeatherData={weatherDataSamples[0]} tmrWeatherData={weatherDataSamples[1]} />
          </div>
          <div className="w-3/5 p-4">
              <ForecastBoard weatherDataArray={weatherDataSamples} />
          </div>
      </div>
  );
};

export default App;
