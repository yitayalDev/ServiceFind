import 'package:flutter/material.dart';
import 'package:service_finder/features/home/home_page.dart';

/// Root widget of the ServiceFind Flutter application.
///
/// The app shell is intentionally minimal at this step: it defines the theme,
/// title, and a placeholder home screen. Navigation routes and feature
/// modules are wired up in later steps.
class ServiceFinderApp extends StatelessWidget {
  const ServiceFinderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ServiceFind',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00695C),
        ),
        useMaterial3: true,
      ),
      // Placeholder home screen; real feature routes are added later.
      home: const HomePage(),
    );
  }
}
