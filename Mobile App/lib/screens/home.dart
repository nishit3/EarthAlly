import 'package:flutter/material.dart';

import 'notifications.dart';

class HomeScreen extends StatelessWidget {
  final Map<String, dynamic> data = {
    "areaUID": "a1",
    "cam_modules": {
      "a1c1": "New CG Rd, Chandkheda, Ahmedabad, Gujarat 382424",
      "a1c2": "4D Square Mall, Motera, Ahmedabad, Gujarat 380005"
    },
    "weather_condition": "rain",
    "soil_modules": {
      "m1": {
        "address": "Mahavir nagar",
        "moisture": 20
      },
      "m2": {
        "address": "Visat Circle",
        "moisture": 50
      }
    },
    "details": {
      "name": "Sabarmati",
      "address": "Sabarmati, Ahmedabad, Gujarat, India 380005",
      "lng": 72.5854508811074,
      "lat": 23.0906672740375
    },
    "water_modules": {
      "m1": {
        "TDS": 25000,
        "address": "ONGC avani bhavan",
        "pH": 13,
        "turbidity": 4
      }
    },
    "deforestation_index": 31.7592083122992,
    "aqi_modules": {
      "m1": {
        "temp": 33,
        "address": "Visat Circle",
        "O3": 23.55999947,
        "CO": 0.629999995,
        "NO2": 15.35999966,
        "humd": 64,
        "PM2.5": 50.95000076,
        "SO2": 43.13000107,
        "NH3": 6.380000114,
        "AQI": 70,
        "aqi_forecast": 101,
        "PM10": 63.95999908,
        "significant_pollutant": "PM2.5"
      }
    },
    "wind_speed": 9.2
  };

   HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
        actions: [
          IconButton(
              onPressed: (){
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => NotificationsScreen(),
                  ),
                );
              },
              icon: Icon(Icons.notifications_active)
          )
        ],
      ),
      body: ListView(
        padding: EdgeInsets.all(8.0),
        children: [
          Card(
            margin: EdgeInsets.symmetric(vertical: 8.0),
            child: ListTile(
              title: Text('Area Details'),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  buildAttributeText('Name: ', data['details']['name']),
                  buildAttributeText('Address: ', data['details']['address']),
                  buildAttributeText('Weather Condition: ', data['weather_condition']),
                  buildAttributeText('Wind Speed: ', '${data['wind_speed'].toStringAsFixed(2)} m/s'),
                ],
              ),
            ),
          ),
          ...buildSoilCards(data['soil_modules']),
          ...buildWaterCards(data['water_modules']),
          ...buildAQICards(data['aqi_modules']),
        ],
      ),
    );
  }

  Widget buildAttributeText(String attribute, String value) {
    return Text.rich(
      TextSpan(
        children: [
          TextSpan(
            text: attribute,
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          TextSpan(
            text: value,
          ),
        ],
      ),
    );
  }

  List<Widget> buildSoilCards(Map<String, dynamic> soilModules) {
    List<Widget> cards = [];
    soilModules.forEach((key, value) {
      cards.add(
        Card(
          margin: EdgeInsets.symmetric(vertical: 8.0),
          child: ListTile(
            title: Text('Soil Module: $key'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                buildAttributeText('Address: ', value['address']),
                buildAttributeText('Moisture: ', '${value['moisture']}%'),
              ],
            ),
          ),
        ),
      );
    });
    return cards;
  }

  List<Widget> buildWaterCards(Map<String, dynamic> waterModules) {
    List<Widget> cards = [];
    waterModules.forEach((key, value) {
      cards.add(
        Card(
          margin: EdgeInsets.symmetric(vertical: 8.0),
          child: ListTile(
            title: Text('Water Module: $key'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                buildAttributeText('Address: ', value['address']),
                buildAttributeText('TDS: ', '${value['TDS']} ppm'),
                buildAttributeText('pH: ', '${value['pH'].toStringAsFixed(2)}'),
                buildAttributeText('Turbidity: ', '${value['turbidity'].toStringAsFixed(2)} NTU'),
              ],
            ),
          ),
        ),
      );
    });
    return cards;
  }

  List<Widget> buildAQICards(Map<String, dynamic> aqiModules) {
    List<Widget> cards = [];
    aqiModules.forEach((key, value) {
      cards.add(
        Card(
          margin: EdgeInsets.symmetric(vertical: 8.0),
          child: ListTile(
            title: Text('AQI Module: $key'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                buildAttributeText('Address: ', value['address']),
                buildAttributeText('Temperature: ', '${value['temp']}°C'),
                buildAttributeText('O3: ', '${value['O3'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('CO: ', '${value['CO'].toStringAsFixed(2)} mg/m³'),
                buildAttributeText('NO2: ', '${value['NO2'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('Humidity: ', '${value['humd']}%'),
                buildAttributeText('PM2.5: ', '${value['PM2.5'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('SO2: ', '${value['SO2'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('NH3: ', '${value['NH3'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('AQI: ', '${value['AQI']}'),
                buildAttributeText('AQI Forecast: ', '${value['aqi_forecast']}'),
                buildAttributeText('PM10: ', '${value['PM10'].toStringAsFixed(2)} µg/m³'),
                buildAttributeText('Significant Pollutant: ', value['significant_pollutant']),
              ],
            ),
          ),
        ),
      );
    });
    return cards;
  }
}
