# NavEx
Navigation + Execution 



### Setup and Run
Prerequisites
 - Python 3.13+
 - Poetry (https://python-poetry.org/docs/)

1. Installation
  - Clone the repo

2. Install dependencies:
   
`poetry install`

3. Environment Variables
Create a .env file in the project root with the following example content:

```
    LOG_LEVEL=INFO
    AUTH_PUBLIC_KEY_FILE_PATH=public.key
    AUTH_AUDIENCE=api-navex-client
    AUTH_ISSUER=api.navex.com
```
4. Generating RSA Keys
To generate the public/private key pair used for authentication, run the shell script:
  `./generate_rsa_keys.sh`

4. Running the app
To start the FastAPI app with hot reload:

`poetry run uvicorn app.main:app --reload`
