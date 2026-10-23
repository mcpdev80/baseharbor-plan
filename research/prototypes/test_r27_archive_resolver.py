import hashlib
import json
import pathlib
import tempfile
import unittest
from r27_archive_resolver import ArchiveError, resolve


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = pathlib.Path(self.tmp.name) / 'evidence' / 'v0.4.27' / 'candidate' / 'run-1'
        (self.directory / 'payloads').mkdir(parents=True)
        self.payload = b'{"status":"ok"}'
        (self.directory / 'payloads' / 'check.json').write_bytes(self.payload)
        self.manifest = {'schema': 'baseharbor.ci-evidence-archive/v1', 'release': 'v0.4.27',
                         'checks': [{'payload': 'payloads/check.json', 'bytes': len(self.payload),
                                     'sha256': hashlib.sha256(self.payload).hexdigest()}]}
        self.save()

    def save(self):
        data = json.dumps(self.manifest, sort_keys=True).encode()
        (self.directory / 'manifest.json').write_bytes(data)
        self.digest = hashlib.sha256(data).hexdigest()

    def resolve(self):
        return resolve(self.tmp.name, 'v0.4.27', 'candidate', 'run-1', self.digest)

    def test_valid_integrity_only(self):
        self.assertEqual(len(self.resolve()['checks']), 1)

    def test_tampered_payload(self):
        (self.directory / 'payloads' / 'check.json').write_bytes(b'bad')
        with self.assertRaises(ArchiveError): self.resolve()

    def test_missing_payload(self):
        (self.directory / 'payloads' / 'check.json').unlink()
        with self.assertRaises(ArchiveError): self.resolve()

    def test_wrong_manifest_digest(self):
        with self.assertRaises(ArchiveError):
            resolve(self.tmp.name, 'v0.4.27', 'candidate', 'run-1', '0' * 64)

    def test_path_traversal(self):
        self.manifest['checks'][0]['payload'] = 'payloads/../manifest.json'
        self.save()
        with self.assertRaises(ArchiveError): self.resolve()

    def test_duplicate_payload(self):
        self.manifest['checks'].append(dict(self.manifest['checks'][0]))
        self.save()
        with self.assertRaises(ArchiveError): self.resolve()

    def test_symlink_payload(self):
        p = self.directory / 'payloads' / 'check.json'
        p.unlink()
        p.symlink_to(self.directory / 'manifest.json')
        with self.assertRaises(ArchiveError): self.resolve()

    def test_symlink_payload_directory(self):
        payload_dir = self.directory / 'payloads'
        (payload_dir / 'check.json').unlink()
        payload_dir.rmdir()
        payload_dir.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaises(ArchiveError): self.resolve()

    def test_wrong_release(self):
        self.manifest['release'] = 'v0.4.26'
        self.save()
        with self.assertRaises(ArchiveError): self.resolve()


if __name__ == '__main__':
    unittest.main()
