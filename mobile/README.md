# MirageGrid — iPhone & Android

Open a circuit on this phone across 25 mesh peers. Offline. No analytics.
Light and dark follow the phone. Author: Aziel Eliab.

Application id: `com.azieeliab.miragegrid`

## Start

1. `cd mobile && flutter create --org com.azieeliab --project-name miragegrid .`
2. `flutter pub get && flutter run`
3. Choose **Open a circuit**.

The SOCKS5 proxy stays in the desktop package (`miragegrid vpn`).

## Open in Android Studio / Xcode

The `android/` and `ios/` folders here are skeleton READMEs because
this tree was written without the Flutter SDK on PATH.

```bash
cd mobile
flutter create --org com.azieeliab --project-name miragegrid .
flutter pub get
flutter run
```

Then open `android/` in Android Studio, or `ios/Runner.xcworkspace` in
Xcode.

## Scope

This phone app assigns a mesh circuit and shows hops. The full userspace
SOCKS5 VPN runs in the desktop package (`miragegrid vpn`).

## Desktop package (counted download)

This phone app does not replace the desktop package.

# → https://miragegrid-download-tracker.vibelock.workers.dev/ ←

GitHub: https://github.com/AzielEliab/miragegrid

**Forks are welcome and always allowed.**
