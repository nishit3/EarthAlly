import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class NotificationsScreen extends StatelessWidget {
  final Map<String, dynamic> notifications = {
    "alerts": [
      {
        "areaUID": "a1",
        "alertUID": "S29-07-202413:46:50a1",
        "Message": "Dust storm is highly possible in Mahavir nagar, Sabarmati, Ahmedabad, Gujarat, India 380005",
        "DateTime": "29-07-2024 13:46:50"
      },
    ]
  };

  @override
  Widget build(BuildContext context) {
    List<dynamic> alerts = notifications['alerts'];

    // Sort the alerts by DateTime, latest first
    alerts.sort((a, b) {
      DateTime dateA = DateFormat('dd-MM-yyyy HH:mm:ss').parse(a['DateTime']);
      DateTime dateB = DateFormat('dd-MM-yyyy HH:mm:ss').parse(b['DateTime']);
      return dateB.compareTo(dateA);
    });

    return Scaffold(
      appBar: AppBar(
        title: Text('Alerts'),
      ),
      body: ListView.builder(
        padding: EdgeInsets.all(8.0),
        itemCount: alerts.length,
        itemBuilder: (context, index) {
          return Card(
            margin: EdgeInsets.symmetric(vertical: 8.0),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10.0),
              side: BorderSide(color: Colors.grey, width: 1.0),
            ),
            child: Padding(
              padding: EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    alerts[index]['Message'],
                    style: TextStyle(fontSize: 16.0),
                  ),
                  SizedBox(height: 4.0),
                  Text(
                    alerts[index]['DateTime'],
                    style: TextStyle(color: Colors.grey),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
