import 'package:flutter/material.dart';

/// Calm paper / charcoal with Aziel gold focus. Follows the system theme.
const Color kGold = Color(0xFFC9A227);
const Color kInk = Color(0xFF1C1915);
const Color kPaper = Color(0xFFF4F0E6);
const Color kNight = Color(0xFF12110E);
const Color kNightPanel = Color(0xFF1C1A16);
const Color kIvory = Color(0xFFF6F1E6);

ThemeData _base({
  required Brightness brightness,
  required ColorScheme scheme,
  required Color scaffold,
  required Color panel,
}) {
  return ThemeData(
    useMaterial3: true,
    brightness: brightness,
    colorScheme: scheme,
    scaffoldBackgroundColor: scaffold,
    appBarTheme: AppBarTheme(
      backgroundColor: scaffold,
      foregroundColor: scheme.onSurface,
      elevation: 0,
      centerTitle: false,
    ),
    cardTheme: CardThemeData(
      color: panel,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: scheme.outline),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        minimumSize: const Size.fromHeight(48),
        backgroundColor: scheme.primary,
        foregroundColor: scheme.onPrimary,
      ),
    ),
    focusColor: kGold,
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: panel,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(10),
        borderSide: const BorderSide(color: kGold, width: 2),
      ),
    ),
  );
}

ThemeData buildLightTheme() {
  const scheme = ColorScheme.light(
    primary: kInk,
    onPrimary: kPaper,
    secondary: kGold,
    onSecondary: kInk,
    surface: Color(0xFFFFFDF8),
    onSurface: kInk,
    outline: Color(0xFFE3D9C4),
  );
  return _base(
    brightness: Brightness.light,
    scheme: scheme,
    scaffold: kPaper,
    panel: const Color(0xFFFFFDF8),
  );
}

ThemeData buildDarkTheme() {
  const scheme = ColorScheme.dark(
    primary: kGold,
    onPrimary: kInk,
    secondary: kGold,
    onSecondary: kInk,
    surface: kNightPanel,
    onSurface: kIvory,
    outline: Color(0xFF3A342A),
  );
  return _base(
    brightness: Brightness.dark,
    scheme: scheme,
    scaffold: kNight,
    panel: kNightPanel,
  );
}

/// Kept so older imports still resolve. New UI uses light + dark.
ThemeData buildAppTheme() => buildDarkTheme();
