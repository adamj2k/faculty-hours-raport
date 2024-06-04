from fastapi import HTTPException, status


class FeatureNotFindException(HTTPException):
    def __init__(
        self, status_code=status.HTTP_404_NOT_FOUND, detail: str = "Feature not found"
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.status_code, self.detail)
