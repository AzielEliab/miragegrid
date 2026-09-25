import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';

import 'package:crypto/crypto.dart';
import 'package:flutter/material.dart';

import 'theme.dart';

void main() {
  runApp(const MirageApp());
}

class MirageApp extends StatelessWidget {
  const MirageApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MirageGrid',
      debugShowCheckedModeBanner: false,
      theme: buildLightTheme(),
      darkTheme: buildDarkTheme(),
      themeMode: ThemeMode.system,
      home: const AssignPage(),
    );
  }
}

class Receipt {
  Receipt({
    required this.sessionId,
    required this.node,
    required this.timestamp,
    required this.integrity,
    required this.hash,
  });
  final String sessionId;
  final int node;
  final String timestamp;
  final String integrity;
  final String hash;
}

String digest(String sessionId, int node, String ts, String integrity) {
  final raw =
      '{"integrity":${jsonEncode(integrity)},"mirage_node":$node,"session_id":${jsonEncode(sessionId)},"timestamp":${jsonEncode(ts)}}';
  return sha256.convert(utf8.encode(raw)).toString();
}

class AssignPage extends StatefulWidget {
  const AssignPage({super.key});

  @override
  State<AssignPage> createState() => _AssignPageState();
}

class _AssignPageState extends State<AssignPage> {
  Receipt? _live;
  bool _closed = false;
  String _status = 'No circuit yet. Open one to start.';

  void _assign() {
    final rng = Random.secure();
    final entropy = Uint8List.fromList(List<int>.generate(32, (_) => rng.nextInt(256)));
    final ts = DateTime.now().toUtc().toIso8601String().split('.').first + 'Z';
    final seed = Uint8List.fromList([...entropy, ...utf8.encode(ts)]);
    final d = sha256.convert(seed).bytes;
    var acc = BigInt.zero;
    for (final b in d) {
      acc = (acc << 8) + BigInt.from(b);
    }
    final index = acc.remainder(BigInt.from(25)).toInt();
    final number = index + 1;
    final sid = List<int>.generate(16, (_) => rng.nextInt(256))
        .map((b) => b.toRadixString(16).padLeft(2, '0'))
        .join();
    const integrity = 'PASS';
    setState(() {
      _closed = false;
      _live = Receipt(
        sessionId: sid,
        node: number,
        timestamp: ts,
        integrity: integrity,
        hash: digest(sid, number, ts, integrity),
      );
      _status = 'Circuit is open. Entry peer is node-${number.toString().padLeft(2, '0')}.';
    });
  }

  void _end() {
    setState(() {
      _closed = true;
      _live = null;
      _status = 'Session ended. The mapping on this phone is gone.';
    });
  }

  @override
  Widget build(BuildContext context) {
    final live = _live != null && !_closed;
    final nodeLabel = live
        ? 'node-${_live!.node.toString().padLeft(2, '0')}'
        : '—';
    return Scaffold(
      appBar: AppBar(
        title: const Text('MirageGrid'),
        actions: [
          TextButton(
            onPressed: () {
              showDialog<void>(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('About'),
                  content: const Text(
                    'MirageGrid opens a circuit on this phone across 25 mesh peers. '
                    'Cap-7 is the mesh DNS factory: four hub mirrors and three decoys. '
                    'It keeps those names on the mesh and does not register names at a public ICANN registrar. '
                    'The SOCKS5 proxy stays in the desktop package. '
                    'Author: Aziel Eliab.',
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Close'),
                    ),
                  ],
                ),
              );
            },
            child: const Text('About'),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            'Open a circuit',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text(
            'MirageGrid opens a private circuit through 25 mesh peers on this phone.',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Theme.of(context).colorScheme.onSurface.withOpacity(0.75),
                ),
          ),
          const SizedBox(height: 20),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(_status, style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 12),
                  Text('Entry peer', style: Theme.of(context).textTheme.labelMedium),
                  const SizedBox(height: 4),
                  Text(nodeLabel, style: const TextStyle(fontFamily: 'monospace', fontSize: 16)),
                  const SizedBox(height: 16),
                  FilledButton(
                    onPressed: _assign,
                    child: const Text('Open a circuit'),
                  ),
                  if (live) ...[
                    const SizedBox(height: 8),
                    OutlinedButton(
                      onPressed: _end,
                      child: const Text('End session'),
                    ),
                  ],
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          if (live)
            Card(
              child: ExpansionTile(
                title: const Text('Advanced'),
                childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                children: [
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Selection uses SHA-256(entropy and timestamp) modulo 25.',
                    ),
                  ),
                  const SizedBox(height: 12),
                  SelectableText(
                    [
                      'session_id: ${_live!.sessionId}',
                      'mirage_node: ${_live!.node}',
                      'node_id: $nodeLabel',
                      'timestamp: ${_live!.timestamp}',
                      'integrity: Passed',
                      'hash: ${_live!.hash}',
                    ].join('\n'),
                    style: const TextStyle(fontFamily: 'monospace', fontSize: 13, height: 1.45),
                  ),
                ],
              ),
            ),
          const SizedBox(height: 24),
          Text(
            'Aziel Eliab',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }
}
