# MirageGrid — iPhone & Android

Assign a mesh circuit (entry 1–25 plus onion hops) via
SHA-256(entropy||timestamp) and mint an in-memory receipt. End session
destroys the mapping.

Companion to the desktop **node-mesh VPN**. Offline. No analytics.
Dark matte / gold.

Application id: `com.azieeliab.miragegrid`

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
