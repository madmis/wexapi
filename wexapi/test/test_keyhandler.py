import unittest
import tempfile
from wexapi.keyhandler import KeyData, AbstractKeyHandler, KeyHandler, InvalidNonceException


class TestKeyData(unittest.TestCase):
    def test_set_nonce(self):
        data = KeyData('secret', 1)

        # happy path
        new_nonce = 28
        self.assertEqual(data.set_nonce(new_nonce), new_nonce)

        # negative nonce
        self.assertRaises(InvalidNonceException, data.set_nonce, 0)

        # non-increasing nonce
        self.assertRaises(InvalidNonceException, data.set_nonce, new_nonce)

        # over the max value
        self.assertRaises(InvalidNonceException, data.set_nonce, 4294967295)

    def test_increment_nonce(self):
        # happy path
        self.assertEqual(KeyData('secret', 1).increment_nonce(), 2)

        # over the max value
        data = KeyData('secret', 4294967294)
        self.assertRaises(InvalidNonceException, data.increment_nonce)


# we need a dummy key handler class to test on
class DummyKeyHandler(AbstractKeyHandler):
    def __init__(self):
        self.keys_loaded = False
        self.datastore_updated = False
        super().__init__()

    def _load_keys(self):
        self.keys_loaded = True

    def _update_data_store(self):
        self.datastore_updated = True


class TestAbstractKeyHandler(unittest.TestCase):
    def test_init(self):
        # test it loads the keys from the datastore
        handler = DummyKeyHandler()
        assert handler.keys_loaded

    def test_keys(self):
        # incidentally tests addKey, too
        self.assertEqual(set(self._handler_with_keys().keys), {'k2', 'k1'})

    def test___del__(self):
        handler = DummyKeyHandler()
        handler.__del__()
        assert handler.datastore_updated

    def test___exit__(self):
        handler = DummyKeyHandler()
        handler.__exit__('type', 'value', 'traceback')
        assert handler.datastore_updated

    def test_close(self):
        handler = DummyKeyHandler()
        handler.close()
        assert handler.datastore_updated

    def test___enter__(self):
        handler = DummyKeyHandler()
        self.assertEqual(handler.__enter__(), handler)

    def test_get_key(self):
        handler = self._handler_with_keys()

        # happy path
        self.assertEqual(handler.get_key('k1').nonce, 3)

        # unknown key
        self.assertRaises(KeyError, handler.get_next_nonce, 'i_dont_exist')

    def test_get_next_nonce(self):
        self.assertEqual(self._handler_with_keys().get_next_nonce('k2'), 29)

    def test_set_next_nonce(self):
        self.assertEqual(self._handler_with_keys().set_next_nonce('k1', 82), 82)

    def _handler_with_keys(self):
        handler = DummyKeyHandler()
        return handler.add_key('k1', 'secret1', 3).add_key('k2', 'secret2', 28)


class TestKeyHandler(unittest.TestCase):
    def test_save(self):
        _, filename = tempfile.mkstemp()

        handler = KeyHandler(filename=filename)
        handler.add_key('k1', 'secret1', 3).add_key('k2', 'secret2', 28)

        handler.close()

        allowed_content = ('k2\nsecret2\n28\nk1\nsecret1\n3\n', 'k1\nsecret1\n3\nk2\nsecret2\n28\n')
        with open(filename) as saved_file:
            self.assertTrue(saved_file.read() in allowed_content)

    def test_parse(self):
        _, filename = tempfile.mkstemp()

        with open(filename, 'w') as input_file:
            input_file.write('k2\nsecret2\n28\nk1\nsecret1\n3\n')

        handler = KeyHandler(filename=filename)

        self.assertEqual(set(handler.keys), {'k2', 'k1'})


if __name__ == '__main__':
    unittest.main()
