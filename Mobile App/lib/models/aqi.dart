class AQIModule{
  double temp;
  double O3;
  double CO;
  double NO2;
  final String address;
  double humd;
  double PM25;
  double PM10;
  double SO2;
  double NH3;
  double AQI;
  double aqi_forecast;
  final String significant_pollutant;

  AQIModule({
    required this.address,
    required this.AQI,
    required this.aqi_forecast,
    required this.CO,
    required this.humd,
    required this.NH3,
    required this.NO2,
    required this.O3,
    required this.PM10,
    required this.PM25,
    required this.significant_pollutant,
    required this.SO2,
    required this.temp,
  }){
    CO = double.parse(CO.toStringAsFixed(2));
    humd = double.parse(humd.toStringAsFixed(2));
    NH3 = double.parse(NH3.toStringAsFixed(2));
    NO2 = double.parse(NO2.toStringAsFixed(2));
    O3 = double.parse(O3.toStringAsFixed(2));
    PM10 = double.parse(PM10.toStringAsFixed(2));
    PM25 = double.parse(PM25.toStringAsFixed(2));
    SO2 = double.parse(SO2.toStringAsFixed(2));
    temp = double.parse(temp.toStringAsFixed(2));
  }

}