"""Exercise Make's setup sequencing without external services."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ApmSetupTests(unittest.TestCase):
    def run_setup(self, target, fail=""):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Makefile").write_text((ROOT / "Makefile").read_text())
            stub = root / "command"
            stub.write_text('''#!/bin/sh
case "$1" in
  install) step=install ;;
  compile) step=compile ;;
  *) step=hydrate ;;
esac
printf '%s\\n' "$step" >> "$EVENTS"
[ "$step" != "$FAIL" ]
''')
            stub.chmod(0o755)
            (root / "uv").symlink_to(stub)
            events = root / "events"
            env = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}",
                       EVENTS=str(events), FAIL=fail)
            results = []
            for _ in range(2):
                results.append(subprocess.run(
                    ["make", "-j8", target, f"APM={stub}"], cwd=root,
                    env=env, capture_output=True, text=True))
            return results, events.read_text().splitlines()

    def test_install_and_update_repeat_in_order(self):
        for target in ("apm-install", "apm-update"):
            with self.subTest(target=target):
                results, events = self.run_setup(target)
                self.assertTrue(all(r.returncode == 0 for r in results), results)
                self.assertEqual(events, ["install", "hydrate", "compile"] * 2)

    def test_failure_stops_later_steps(self):
        for target in ("apm-install", "apm-update"):
            for failure, expected in (("install", ["install"]),
                                      ("hydrate", ["install", "hydrate"])):
                with self.subTest(target=target, failure=failure):
                    results, events = self.run_setup(target, failure)
                    self.assertTrue(all(r.returncode != 0 for r in results))
                    self.assertEqual(events, expected * 2)

    def test_compile_is_independent(self):
        results, events = self.run_setup("apm-compile")
        self.assertTrue(all(r.returncode == 0 for r in results))
        self.assertEqual(events, ["compile"] * 2)
