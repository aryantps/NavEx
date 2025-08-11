#!/bin/bash

# ===============================
# reusable script that generates a 2048-bit RSA key pair for RS256.
# ===============================

PRIVATE_KEY_PATH="./private.key"
PUBLIC_KEY_PATH="./public.key"

echo "Generating RSA private key..."
openssl genpkey -algorithm RSA -out "$PRIVATE_KEY_PATH" -pkeyopt rsa_keygen_bits:2048

if [ $? -ne 0 ]; then
  echo "❌ Failed to generate private key."
  exit 1
fi
echo "✅ Private key saved to: $PRIVATE_KEY_PATH"


echo "Generating public key from private key..."
openssl rsa -in "$PRIVATE_KEY_PATH" -pubout -out "$PUBLIC_KEY_PATH"

if [ $? -ne 0 ]; then
  echo "❌ Failed to generate public key."
  exit 1
fi
echo "✅ Public key saved to: $PUBLIC_KEY_PATH"

echo "🎉 Key generation complete!"
