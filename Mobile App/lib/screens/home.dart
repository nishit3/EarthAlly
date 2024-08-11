import 'dart:async';
import 'dart:convert';
import 'package:earth_ally/models/aqi.dart';
import 'package:earth_ally/models/area.dart';
import 'package:earth_ally/models/soil.dart';
import 'package:earth_ally/models/water.dart';
import 'package:earth_ally/screens/alerts.dart';
import 'package:earth_ally/widgets/aqi.dart';
import 'package:earth_ally/widgets/area.dart';
import 'package:earth_ally/widgets/soil.dart';
import 'package:earth_ally/widgets/water.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class HomeScreen extends StatefulWidget {
  final String areaUID;
  const HomeScreen({super.key, required this.areaUID});

  @override
  State<HomeScreen> createState() {
    return _HomeScreenState();
  }
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isLoading = true;
  List<AQIModule> aqiModulesList = [];
  List<WaterModule> waterModulesList = [];
  List<SoilModule> soilModulesList = [];
  late Area area;
  String areaName = "";

  Future<dynamic> _fetchAreaData() async {
    final response = await http.get(
      Uri.parse(
          'https://ENDPOINT/prod/get-specific-area-data?areaUID=${widget.areaUID}'),
    );
    final responseBody = await jsonDecode(response.body);
    return responseBody;
  }

  void _updateData() async {
    final responseBody = await _fetchAreaData();
    areaName = responseBody["details"]["name"];
    aqiModulesList = [];
    waterModulesList = [];
    soilModulesList = [];

    //fetch area information
    area = Area(
        address: responseBody["details"]["address"],
        name: responseBody["details"]["name"],
        weather_condition: responseBody["weather_condition"],
        wind_speed: responseBody["wind_speed"]);

    // fetch aqi modules data
    final aqiModules = responseBody["aqi_modules"] as Map;
    final aqiModuleKeys = aqiModules.keys;
    for (final aqiModuleKey in aqiModuleKeys) {
      final aqiModuleData = aqiModules[aqiModuleKey];
      aqiModulesList.add(AQIModule(
          address: aqiModuleData["address"],
          AQI: aqiModuleData["AQI"],
          aqi_forecast: aqiModuleData["aqi_forecast"],
          CO: aqiModuleData["CO"],
          humd: aqiModuleData["humd"],
          NH3: aqiModuleData["NH3"],
          NO2: aqiModuleData["NO2"],
          O3: aqiModuleData["O3"],
          PM10: aqiModuleData["PM10"],
          PM25: aqiModuleData["PM2.5"],
          significant_pollutant: aqiModuleData["significant_pollutant"],
          SO2: aqiModuleData["SO2"],
          temp: aqiModuleData["temp"]));

      // fetch water modules data
      final waterModules = responseBody["water_modules"] as Map;
      final waterModuleKeys = waterModules.keys;
      for (final waterModuleKey in waterModuleKeys) {
        final waterModuleData = waterModules[waterModuleKey];
        waterModulesList.add(WaterModule(
            address: waterModuleData["address"],
            pH: waterModuleData["pH"],
            TDS: waterModuleData["TDS"],
            turbidity: waterModuleData["turbidity"]));

        // fetch soil modules data
        final soilModules = responseBody["soil_modules"] as Map;
        final soilModuleKeys = soilModules.keys;
        for (final soilModuleKey in soilModuleKeys) {
          final soilModuleData = soilModules[soilModuleKey];
          soilModulesList.add(SoilModule(
              address: soilModuleData["address"],
              moisture: soilModuleData["moisture"]));
        }

        // this if block is temp solution for areaUID a2
        if(soilModulesList.length > 1)
          {
            if(soilModulesList[0].address == soilModulesList[1].address)
            {
              soilModulesList.removeAt(1);
            }
          }

        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  void initState() {
    _updateData();
    Timer.periodic(const Duration(seconds: 5), (timer) {_updateData();});
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          actions: [
            IconButton(
                onPressed: (){
                  Navigator.of(context).push(MaterialPageRoute(builder: (context) => AlertsScreen(areaUID: widget.areaUID,),));
                },
                icon: const Icon(Icons.notification_important_sharp, color: Colors.white,)
            )
          ],
          backgroundColor: Colors.green,
          title: Text(
            areaName == "" ? "Dashboard" : areaName,
            style: const TextStyle(color: Colors.white),
          ),
        ),
        backgroundColor: const Color.fromARGB(255, 227, 225, 225),
        body: Center(
            child: _isLoading
                ? const CircularProgressIndicator(
                    color: Colors.green,
                  )
                : SingleChildScrollView(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          AreaCard(area: area),
                          const SizedBox(
                            height: 15,
                          ),
                          AQICard(aqiModules: aqiModulesList),
                          const SizedBox(
                            height: 10,
                          ),
                          WaterCard(waterModules: waterModulesList),
                          const SizedBox(
                            height: 10,
                          ),
                          SoilCard(soilModules: soilModulesList),
                        ],
                      ),
                    ),
                  )));
  }
}
