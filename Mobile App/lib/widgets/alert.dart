import 'package:earth_ally/models/alert.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class IndividualAlert extends StatelessWidget{

  final Alert alert;
  const IndividualAlert({super.key, required this.alert});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.fromLTRB(6, 6, 6, 7),
          decoration: const BoxDecoration(
              border: Border.fromBorderSide(BorderSide(
                  style: BorderStyle.solid,
                  width: 1,
                  color: CupertinoColors.black)
              )
          ),

          child: Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              const Icon(Icons.notifications_active_outlined, size: 33,),
              const SizedBox(
                width: 25,
              ),
              Expanded(
                child: Column(
                  children: [
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        alert.Message,
                        style: const TextStyle(fontSize: 15),
                      ),
                    ),
                    const SizedBox(height: 2,),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        alert.DateTime,
                        style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(
          height: 23,
        ),
      ],
    );
  }

}