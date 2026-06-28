import pymem
import pymem.process

class MemoryInterface:
    """Wrapper for direct process memory access using pymem."""

    def __init__(self, process_name="RobloxPlayerBeta.exe"):
        self.process_name = process_name
        self.pm = None
        self.attach()

    def attach(self):
        try:
            self.pm = pymem.Pymem(self.process_name)
        except pymem.exception.ProcessNotFound:
            raise RuntimeError(
                f"Process '{self.process_name}' not found. Make sure Roblox is running."
            )

    def read_integer(self, address: int) -> int:
        return self.pm.read_int(address)

    def write_int(self, address: int, value: int):
        self.pm.write_int(address, value)

    def read_float(self, address: int) -> float:
        return self.pm.read_float(address)

    def write_float(self, address: int, value: float):
        self.pm.write_float(address, value)

    def read_bytes(self, address: int, length: int) -> bytes:
        return self.pm.read_bytes(address, length)

    def write_bytes(self, address: int, data: bytes):
        self.pm.write_bytes(address, data)

    def is_attached(self) -> bool:
        try:
            self.pm.read_int(0x0)  # test read
            return True
        except:
            return False
