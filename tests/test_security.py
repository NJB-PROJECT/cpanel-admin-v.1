import unittest
import os
import shutil
from app.utils.apache_manager import is_valid_domain, create_domain, delete_domain
from app.config import Config

class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        # Ensure we are in development mode for safety
        Config.MODE = 'development'
        os.makedirs(Config.WEB_ROOT, exist_ok=True)
        os.makedirs(Config.APACHE_SITES_AVAILABLE, exist_ok=True)

    def tearDown(self):
        # Clean up mock directories
        if os.path.exists(Config.MOCK_DIR):
            shutil.rmtree(Config.MOCK_DIR)

    def test_domain_validation(self):
        """Test that invalid domains are rejected."""
        valid_domains = ['example.com', 'sub.domain.co.id', 'jarvis-clouding.sbs']
        invalid_domains = [
            '../../etc/passwd',
            '/etc/passwd',
            'example.com; rm -rf /',
            'example.com && ls',
            ' space .com',
            'invalid@char'
        ]

        for d in valid_domains:
            self.assertTrue(is_valid_domain(d), f"Should be valid: {d}")

        for d in invalid_domains:
            self.assertFalse(is_valid_domain(d), f"Should be invalid: {d}")

    def test_create_domain_traversal(self):
        """Test that create_domain fails with traversal attempts."""
        success, msg = create_domain('../../evildomain', 'admin@evil.com')
        self.assertFalse(success)
        self.assertIn("Invalid domain", msg)

    def test_delete_domain_traversal(self):
        """Test that delete_domain fails with traversal attempts."""
        success, msg = delete_domain('../../evildomain')
        self.assertFalse(success)
        self.assertIn("Invalid domain", msg)

if __name__ == '__main__':
    unittest.main()
