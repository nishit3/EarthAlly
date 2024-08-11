import 'dart:convert';
import 'package:earth_ally/screens/home.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;


class LoginScreen extends StatefulWidget
{
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() {
    return _LoginScreenState();
  }
}

class _LoginScreenState extends State<LoginScreen>
{
  bool _isLoading = true;
  final List<DropdownMenuEntry> dropDownMenuItems = [];

  void _fetchAllAreasDetails() async {
    final response = await http.get(
      Uri.parse('https://ENDPOINT/prod/get-areas-basic-information'),
    );
    final responseBody = await jsonDecode(response.body);
    final allAreaDetails = await responseBody["areasBasicInformation"];

    for (final areaDetail in allAreaDetails)
    {
      dropDownMenuItems.add(DropdownMenuEntry(value: areaDetail["areaUID"],
          label: areaDetail["name"]
      ));
    }
    setState(() {
      _isLoading = false;
    });
  }

  @override
  void initState() {
    _fetchAllAreasDetails();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 227, 225, 225),
        body: SingleChildScrollView(
              child: _isLoading ? const Align( alignment: Alignment.center, child: CircularProgressIndicator(color: Colors.green,))
                  :
              Align(
                alignment: Alignment.topCenter,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const SizedBox(height: 70,),
                    Container(
                      padding: const EdgeInsets.only(
                          bottom: 5
                          , left: 15, right: 20, top: 30),
                      width: 300,
                      child: Image.asset("lib/assets/ea_logo.jpg"),
                    ),
                    const SizedBox(height: 40),
                    DropdownMenu(
                        dropdownMenuEntries: dropDownMenuItems,
                        label: const Text("Select Your Area", style: TextStyle(fontWeight: FontWeight.bold)),
                        enableSearch: true,
                        width: 260,
                        requestFocusOnTap: true,
                        enableFilter: true,
                        onSelected: (value) {
                          FocusScope.of(context).unfocus();
                          if(value != null)
                          {
                            Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (context) => HomeScreen(areaUID: value as String,),));
                          }
                        },
                      ),
                  ],
                ),
              )
          ),
        );
  }
}
