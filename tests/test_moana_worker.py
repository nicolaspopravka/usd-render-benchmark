"""Execute the worker against fake Rez/GPU commands and check Docker lifecycle."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PINNED_IMAGE = 'ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:' + 'a' * 64

@unittest.skipUnless(sys.platform.startswith('linux'), 'Worker fixtures require Linux GNU time and cgroups')
class ShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        (self.repo / 'tools').mkdir(parents=True)
        (self.repo / 'packages').mkdir()
        self.scene = self.root / 'scene'
        (self.scene / 'usd').mkdir(parents=True)
        (self.scene / 'usd/island.usda').write_text('#usda 1.0\n')
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=str(self.bin) + ':' + os.environ['PATH'], MOANA_RUNTIME='runpod')
        for name in ('moana_moonray_worker.sh', 'run_moana_moonray.sh'):
            (self.repo / 'tools' / name).write_text((ROOT / 'tools' / name).read_text())

    def tearDown(self):
        self.temp.cleanup()

    def executable(self, name, body):
        path = self.bin / name
        path.write_text(body)
        path.chmod(0o755)

    def test_real_worker_commands_and_exit_status(self):
        self.executable('nvidia-smi', '#!/bin/sh\necho fixture-gpu\n')
        for mode, code in [('default', 0), ('xpu', 139)]:
            out = self.root / mode
            self.executable('rez', f'''#!/bin/sh
case "$*" in *python3*) echo '(25, 5, 1)'; exit 0;; esac
printf '%s\\n' "$@" > "$TMPDIR/../rez-arguments.txt"
printf '%s' 'fixture image' > "$TMPDIR/../island.jpg"
exit {code}
''')
            try:
                result = subprocess.run(['bash', '-x', str(self.repo / 'tools/moana_moonray_worker.sh'), str(self.scene), str(out), mode],
                                        env=self.env, capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired as error:
                self.fail('Worker fixture hung:\n' + (error.stderr or b'').decode())
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertEqual(int((out / 'render-exit.txt').read_text()), code)
            self.assertEqual(int((out / 'worker-exit.txt').read_text()), code)
            arguments = (out / 'rez-arguments.txt').read_text().splitlines()
            if mode == 'xpu':
                self.assertIn('HDMOONRAY_EXEC_MODE=xpu', arguments)
                self.assertIn('REZ_MOONRAY_ROOT=/usr/local', arguments)
                self.assertIn('./tools/usdrecord_egl.py', arguments)
            else:
                self.assertIn('usdrecord', arguments)
                self.assertNotIn('HDMOONRAY_EXEC_MODE=xpu', arguments)
            self.assertIn('/island/cam/shotCam', arguments)
            self.assertTrue((out / 'resources.txt').read_text())
            self.assertIn('Time:', (out / 'time.txt').read_text())
            self.assertEqual((self.scene / 'usd/island.usda').read_text(), '#usda 1.0\n')

    def test_worker_setup_failure_stops_before_render(self):
        self.executable('nvidia-smi', '#!/bin/sh\necho fixture-gpu\n')
        self.executable('rez', '#!/bin/sh\nexit 69\n')
        out = self.root / 'failed'
        result = subprocess.run(['bash', str(self.repo / 'tools/moana_moonray_worker.sh'), str(self.scene), str(out), 'default'],
                                env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 69)
        self.assertFalse((out / 'render-start-utc.txt').exists())
        self.assertEqual((out / 'worker-exit.txt').read_text().strip(), '69')

    def test_docker_adapter_lifecycle_and_shared_worker_wiring(self):
        self.executable('git', '#!/bin/sh\necho fixture-sha\n')
        calls = self.root / 'docker-calls.jsonl'
        self.env['FIXTURE_CALLS'] = str(calls)
        self.executable('docker', '''#!/usr/bin/env python3
import json, os, sys, time
args=sys.argv[1:]
with open(os.environ['FIXTURE_CALLS'], 'a') as f: f.write(json.dumps(args)+'\\n')
operation=args[0]
if operation=='wait':
    if os.environ['FIXTURE_CASE']=='timeout': time.sleep(5)
    print('139' if os.environ['FIXTURE_CASE']=='failure' else '0')
elif operation=='logs': print('fixture log')
elif operation=='inspect': print('{"Running":false}')
else: print('fixture')
''')
        (self.repo / 'runnable_image.txt').write_text(PINNED_IMAGE + '\n')
        for case, expected in [('success', 0), ('failure', 139), ('timeout', 124), ('xpu', 0)]:
            self.env['FIXTURE_CASE'] = case
            args = ['bash', str(self.repo / 'tools/run_moana_moonray.sh'), str(self.scene), '1']
            if case == 'xpu': args.append('xpu')
            result = subprocess.run(args, env=self.env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, expected, result.stderr)
        commands = [json.loads(line) for line in calls.read_text().splitlines()]
        creates = [c for c in commands if c[0] == 'create']
        self.assertEqual(len(creates), 4)
        for create in creates:
            self.assertIn('tools/moana_moonray_worker.sh', create)
            self.assertIn('nofile=65536:65536', create)
            self.assertTrue(any('target=/moana,readonly' in a for a in create))
        self.assertEqual(sum(c[0] == 'stop' for c in commands), 4)
        self.assertFalse(any(c[0] == 'rm' for c in commands))
        outputs = list((self.repo / 'local-runs').iterdir())
        self.assertEqual(len(outputs), 4)
        for out in outputs:
            self.assertEqual((out / 'runtime.txt').read_text().strip(), 'docker')
            self.assertTrue((out / 'container-state.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
