from fastapi import HTTPException, status


class FeatureNotFindException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Feature not found"

    def __init__(self):
        super().__init__(self.status_code, self.detail)
