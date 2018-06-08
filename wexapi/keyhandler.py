class InvalidNonceException(Exception):
    """
    Raised when an invalid nonce is set on a key.
    """
    pass


class KeyData(object):
    # wex.nz API caps nonce's values
    MAX_NONCE_VALUE = 4294967294

    def __init__(self, secret: str, nonce: int):
        self.secret = secret
        self.nonce = nonce

    def set_nonce(self, new_nonce: int) -> int:
        if new_nonce <= 0:
            raise InvalidNonceException('Nonce must be positive')
        if new_nonce <= self.nonce:
            raise InvalidNonceException('Nonce must be strictly increasing')
        if new_nonce > self.MAX_NONCE_VALUE:
            raise InvalidNonceException('Nonce cannot be greater than {}'.format(self.MAX_NONCE_VALUE))

        self.nonce = new_nonce

        return self.nonce

    def increment_nonce(self) -> int:
        if self.nonce >= self.MAX_NONCE_VALUE:
            raise InvalidNonceException('Cannot increment nonce, already at maximum value')

        self.nonce += 1

        return self.nonce


class AbstractKeyHandler(object):
    """
    AbstractKeyHandler handles the tedious task of managing nonce
    associated with wex.nz API key/secret pairs.
    The get_next_nonce method is threadsafe, all others need not be.
    """

    def __init__(self):
        self._keys = {}
        self._load_keys()

    @property
    def keys(self):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        return self._keys.keys()

    def _load_keys(self):
        """ 
        Load the keys with their secrets and nonces from the datastore. 
        """
        raise NotImplementedError

    def _update_data_store(self):
        """
        Should update the datastore with the latest data (newest nonces, and any
        keys that might have been added)
        """
        raise NotImplementedError

    def __del__(self):
        self.close()

    def close(self):
        self._update_data_store()

        # By convention, if _keys is None the object is considered
        # closed and should not attempt to touch the underlying storage.
        self._keys = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()

    def add_key(self, key: str, secret: str, next_nonce: int):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        self._keys[key] = KeyData(secret, next_nonce)
        return self

    def get_next_nonce(self, key: str) -> int:
        return self.get_key(key).increment_nonce()

    def get_secret(self, key: str) -> str:
        return self.get_key(key).secret

    def set_next_nonce(self, key: str, next_nonce: int) -> int:
        return self.get_key(key).set_nonce(next_nonce)

    def get_key(self, key: str):
        if self._keys is None:
            raise Exception("Attempted to use a closed key handler.")

        data = self._keys.get(key)
        if data is None:
            raise KeyError("Key not found: {}".format(key))

        return data


class KeyHandler(AbstractKeyHandler):
    """
    An implementation of AbstractKeyHandler using local files to store the data.
    """

    def __init__(self, filename: str = None, resave_on_deletion: bool = True):
        """
        The given file is assumed to be a text file with three lines (key, secret, nonce) per entry.
        """
        self.filename = filename
        self.resave_on_deletion = resave_on_deletion
        super().__init__()

    def _load_keys(self):
        if self.filename is not None:
            self._load()

    def _update_data_store(self):
        if self.resave_on_deletion and self.filename is not None:
            self._save()

    def _save(self):
        # Do nothing if the object has been closed.
        if self._keys is None:
            return

        with open(self.filename, 'wt') as f:
            for k, data in self._keys.items():
                f.write("%s\n%s\n%d\n" % (k, data.secret, data.nonce))

    def _load(self):
        with open(self.filename, 'rt') as input_file:
            while True:
                key = input_file.readline().strip()
                if not key:
                    break
                secret = input_file.readline().strip()
                nonce = int(input_file.readline().strip())
                self.add_key(key, secret, nonce)
