import 'dart:async';
import 'dart:convert';
import 'package:earth_ally/widgets/alert.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import '../models/alert.dart';


class AlertsScreen extends StatefulWidget {
  final String areaUID;

  const AlertsScreen({super.key, required this.areaUID});

  @override
  State<AlertsScreen> createState() {
    return _AlertScreenState();
  }
}

class _AlertScreenState extends State<AlertsScreen>{

  bool _isLoading = true;
  List<Alert> alerts = [];

  void _updateAlerts() async{
    alerts = [];

    final response = await http.get(
      Uri.parse(
          'https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-alerts?areaUID=${widget.areaUID}'),
    );
    final responseBody = await jsonDecode(response.body);
    final alertsData = await responseBody["alerts"];

    alertsData.sort((a, b) {
      DateTime dateA = DateFormat('dd-MM-yyyy HH:mm:ss').parse(a['DateTime']);
      DateTime dateB = DateFormat('dd-MM-yyyy HH:mm:ss').parse(b['DateTime']);
      return dateB.compareTo(dateA);
    });

    for(final alertData in alertsData){
      alerts.add(Alert(
          DateTime: alertData["DateTime"],
          Message: alertData["Message"]
       )
      );
    }
    setState(() {
      _isLoading = false;
    });
  }

  void _onBackPress()
  {
    Navigator.of(context).pop();
  }

  @override
  void initState() {
    _updateAlerts();
    Timer.periodic(const Duration(seconds: 3), (timer) {_updateAlerts();});
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 227, 225, 225),
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back,color: Colors.white), onPressed: _onBackPress),
        backgroundColor: Colors.green,
        title: const Text("Alerts", style: TextStyle(color: Colors.white),),
      ),
      body: _isLoading? const Center(child: CircularProgressIndicator(color: Colors.green,),)
           :
           alerts.isEmpty?
           const Center(child: Text("No Alerts",style: TextStyle(fontSize: 21,color: Colors.black)),)
               :
           SingleChildScrollView(
             padding: const EdgeInsets.all(10),
             child: Column(
               children: [
                 ...alerts.map((alert) =>
                    IndividualAlert(alert: alert,)
                 )
               ],
             ),
           )
    );
  }

}
