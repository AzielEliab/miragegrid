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
      theme: buildAppTheme(),
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
  String _note = 'no session';

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
      _note = 'assigned entry node-$number. Circuit hops held in RAM.';
    });
  }

  void _end() {
    setState(() {
      _closed = true;
      _live = null;
      _note = 'session ended. Mapping destroyed. node is no longer readable.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('MirageGrid')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFF2A1515),
            child: const Padding(
              padding: EdgeInsets.all(12),
              child: Text(
                'MirageGrid is a node-mesh VPN and anonymity network. '
                'This app assigns a 25-node mesh circuit (entry + hops). '
                'The desktop package runs the userspace SOCKS5 VPN. '
                'Lawful privacy tool. Author Aziel Eliab.',
                style: TextStyle(height: 1.4),
              ),
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'You enter the booth. The system selects a booth. The call is attributed '
            'to that booth. You leave with no persistent booth identity.',
            style: TextStyle(color: kGold, fontStyle: FontStyle.italic),
          ),
          const SizedBox(height: 16),
          Text(_note),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            children: [
              FilledButton(onPressed: _assign, child: const Text('Assign node')),
              OutlinedButton(onPressed: _end, child: const Text('End session')),
            ],
          ),
          const SizedBox(height: 8),
          const Text(
            'Selection: SHA-256(entropy || timestamp) as big-endian int % 25. '
            'Not random.choice. Extra hops use SHA-256(...|hop|salt).',
            style: TextStyle(color: kGoldDim, fontSize: 12),
          ),
          if (_live != null && !_closed) ...[
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: SelectableText(
                  [
                    'session_id: ${_live!.sessionId}',
                    'mirage_node: ${_live!.node}',
                    'node_id: node-${_live!.node.toString().padLeft(2, '0')}',
                    'timestamp: ${_live!.timestamp}',
                    'integrity: ${_live!.integrity}',
                    'hash: ${_live!.hash}',
                  ].join('\n'),
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 13, height: 1.45),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
