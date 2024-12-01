
import React from "react";


class WeatherDataModel {
    day: string;
    date: string;
    temp: string;
    condition: string;
    nightCondition: string;
    subCondition: string;
    icon: string;
    precip: string;
    wind: string;
    windGusts: string;
    airQuality: string;


    constructor(day: string, date: string, temp: string, condition: string, nightCondition: string, subCondition: string, icon: string, precip: string, wind: string, windGusts: string, airQuality: string) {
        this.day = day;
        this.date = date;
        this.temp = temp;
        this.condition = condition;
        this.nightCondition = nightCondition;
        this.subCondition = subCondition;
        this.icon = icon;
        this.precip = precip;
        this.wind = wind;
        this.windGusts = windGusts;
        this.airQuality = airQuality
    }
}

export default WeatherDataModel;