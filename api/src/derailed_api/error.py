class Error(Exception):
    def __init__(self, code: int, reason: str, status_code: int = 400) -> None:
        self.code = code
        self.reason = reason
        self.status_code = status_code

    def to_json(self) -> dict[str, int | str]:
        return {
            "code": self.code,
            "message": self.reason
        }
