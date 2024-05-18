pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
modal token set --token-id $TOKEN_ID --token-secret $TOKEN_SECRET
modal config set-environment dev
