import ctypes
import os
from ctypes import c_void_p, c_char_p, c_bool, c_size_t, c_uint8, create_string_buffer

_lib_path = os.getenv("OBINEXUS_BCI_LIB", "libobinexus_bci.so")
_lib = ctypes.CDLL(_lib_path)

# Signatures
_lib.obinexus_init.restype = c_void_p
_lib.obinexus_init.argtypes = [c_char_p]

_lib.obinexus_shutdown.restype = None
_lib.obinexus_shutdown.argtypes = [c_void_p]

_lib.obinexus_start_stream.restype = c_bool
_lib.obinexus_start_stream.argtypes = [c_void_p]

_lib.obinexus_stop_stream.restype = c_bool
_lib.obinexus_stop_stream.argtypes = [c_void_p]

_lib.obinexus_read_event.restype = c_size_t
_lib.obinexus_read_event.argtypes = [c_void_p, ctypes.POINTER(c_uint8), c_size_t]

_lib.obinexus_write_relay.restype = c_bool
_lib.obinexus_write_relay.argtypes = [c_void_p, ctypes.POINTER(c_uint8), c_size_t]

_lib.obinexus_get_version.restype = c_char_p
_lib.obinexus_get_version.argtypes = [c_void_p]

_lib.obinexus_verify_auraseal.restype = c_bool
_lib.obinexus_verify_auraseal.argtypes = [c_char_p, c_char_p]

_lib.obinexus_load_component_backup.restype = c_bool
_lib.obinexus_load_component_backup.argtypes = [c_void_p, c_char_p]

_lib.obinexus_check_compatibility.restype = c_bool
_lib.obinexus_check_compatibility.argtypes = [c_void_p]

_lib.obinexus_hot_swap_commit.restype = c_bool
_lib.obinexus_hot_swap_commit.argtypes = [c_void_p]

_lib.obinexus_force_rollback.restype = c_bool
_lib.obinexus_force_rollback.argtypes = [c_void_p]

_lib.obinexus_last_error.restype = c_char_p
_lib.obinexus_last_error.argtypes = [c_void_p]

# Friendly wrapper
class OBINexus:
    def __init__(self, config_json=b'{}'):
        self._ctx = _lib.obinexus_init(config_json)
        if not self._ctx:
            raise RuntimeError("Failed to initialize OBINexus runtime")

    def shutdown(self):
        _lib.obinexus_shutdown(self._ctx)

    def start_stream(self):
        return bool(_lib.obinexus_start_stream(self._ctx))

    def stop_stream(self):
        return bool(_lib.obinexus_stop_stream(self._ctx))

    def read_event(self, max_bytes=4096):
        buf = (c_uint8 * max_bytes)()
        n = _lib.obinexus_read_event(self._ctx, buf, max_bytes)
        return bytes(buf[:n])

    def write_relay(self, payload: bytes):
        arr = (c_uint8 * len(payload)).from_buffer_copy(payload)
        return bool(_lib.obinexus_write_relay(self._ctx, arr, len(payload)))

    def get_version(self):
        return _lib.obinexus_get_version(self._ctx).decode('utf-8')

    def verify_auraseal(self, artifact_path, expected_sig):
        return bool(_lib.obinexus_verify_auraseal(artifact_path.encode('utf-8'), expected_sig.encode('utf-8')))

    def load_component_backup(self, artifact_path):
        return bool(_lib.obinexus_load_component_backup(self._ctx, artifact_path.encode('utf-8')))

    def check_compatibility(self):
        return bool(_lib.obinexus_check_compatibility(self._ctx))

    def hot_swap_commit(self):
        return bool(_lib.obinexus_hot_swap_commit(self._ctx))

    def force_rollback(self):
        return bool(_lib.obinexus_force_rollback(self._ctx))

    def last_error(self):
        err = _lib.obinexus_last_error(self._ctx)
        return None if not err else err.decode('utf-8')
