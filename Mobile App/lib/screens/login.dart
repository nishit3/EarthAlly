import 'package:earth_ally/screens/home.dart';
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget
{
  @override
  State<LoginScreen> createState() {
    return _LoginScreenState();
  }
}

class _LoginScreenState extends State<LoginScreen>
{
  String? _selectedValue;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 227, 225, 225),
        body: Center(
          child: SingleChildScrollView(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    padding: const EdgeInsets.only(
                        bottom: 5
                        , left: 15, right: 20, top: 30),
                    width: 300,
                    child: Image.asset("lib/assets/ea_logo.jpg"),
                  ),
                  const SizedBox(height: 40),
                  Container(
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.grey),
                      borderRadius: BorderRadius.circular(5),
                    ),
                    padding: const EdgeInsets.symmetric(horizontal: 15),
                    child: DropdownButton<String>(
                      value: _selectedValue,
                      hint: const Text('Select Your Area'),
                      items: <String>['Sabarmati', 'Chimanlal Girdharlal Rd, Ellisbridge', 'New Textile Market, Surat', 'Polo Forest']
                          .map((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                      onChanged: (String? newValue) {
                        setState(() {
                          _selectedValue = newValue;
                        });
                        if (newValue != null) {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => HomeScreen(),
                            ),
                          );
                        }
                      },
                    ),
                  ),
                ],
              )
          ),
        )

    );
  }
}