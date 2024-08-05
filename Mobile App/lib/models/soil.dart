class SoilModule{

  final String address;
  double moisture;

  SoilModule({
    required this.address,
    required this.moisture
  }){
    moisture = double.parse(moisture.toStringAsFixed(2));
  }

}