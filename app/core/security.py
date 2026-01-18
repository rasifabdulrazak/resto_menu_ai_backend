from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Paste your JWT token here",
)
