class Area{
  String weather_condition;
  final String name;
  final String address;
  double wind_speed;

  Area({
    required this.address,
    required this.name,
    required this.weather_condition,
    required this.wind_speed,
 }){
    wind_speed = double.parse(wind_speed.toStringAsFixed(2));
    weather_condition = weather_condition[0].toUpperCase() + weather_condition.substring(1);
  }

}