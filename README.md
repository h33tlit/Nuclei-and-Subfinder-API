# Nuclei And Subfinder API
Web API for nuclei and subfinder will help you automate your entire security testing workflow since you can host it anywhere and make it accessible for your other applications.

# How to install?

1. Install the requirements with `pip install -r requirements.txt`
2. Launch it with uvicorn `uvicorn app:app --host 0.0.0.0 --port 10000 --timeout-keep-alive 1000 --workers 5` (change the host if you require)

# Usage

To get subdomain results: `http://127.0.0.1/api/scanner1/facebook.com`

To get nuclei results (WITHOUT AUTOSCAN): `http://127.0.0.1/api/v2/scanner2?target_name=http://test.com&autoscan=false&tags=misconfig,cve,panel`

To get nuclei results (WITH AUTOSCAN): `http://127.0.0.1/api/v2/scanner2?target_name=http://test.com&autoscan=true`
