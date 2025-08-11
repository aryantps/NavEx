import jwt
import datetime
import os


PRIVATE_KEY_PATH = "./private_key.pem" # PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "./private_key.pem")
AUDIENCE = os.environ.get("AUTH_AUDIENCE", "default-client-id")
ISSUER = os.environ.get("AUTH_ISSUER", "https://issuer.navex.com")

with open(PRIVATE_KEY_PATH, "r") as f:
    private_key = f.read()

payload = {
    "sub": "user123",
    "roles": "admin,editor",
    "iss": ISSUER,
    "aud": AUDIENCE,
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=500)
}

token = jwt.encode(
    payload,
    private_key,
    algorithm="RS256"
)

print("Generated JWT:\n")
print(token)
