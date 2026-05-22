Run the Atlas AI demo setup: seed the database and create Atlas Vector Search indexes.

## What this command does

1. Checks that `.env` has real (non-placeholder) credentials
2. If credentials are missing or placeholder, asks the user to provide them and writes them to `.env`
3. Runs `python scripts/setup.py` and streams the output
4. Reports success or failure clearly

## Steps

### 1 — Check credentials

Run:
```
python3 -c "
import re, os
with open('.env') as f: c = f.read()
def get(key):
    m = re.search(r'^' + key + r'=(.+)$', c, re.MULTILINE)
    return m.group(1).strip('\"').strip(\"'\") if m else ''
uri = get('MONGODB_URI')
key = get('VOYAGE_API_KEY')
def placeholder(v):
    return not v or 'USERNAME:PASSWORD' in v or 'YOUR-CLUSTER' in v or 'xxxxxxxx' in v
print('uri_ok=' + str(not placeholder(uri)))
print('key_ok=' + str(not placeholder(key)))
print('uri_preview=' + (uri[:40] + '...' if len(uri) > 40 else uri))
print('key_preview=' + (key[:12] + '...' if len(key) > 12 else key))
"
```

If `.env` does not exist, tell the user to run `./setup.sh` first (it creates `.env` and installs dependencies).

### 2 — Handle missing credentials

For each credential that is missing or placeholder:

**MONGODB_URI missing:**
Tell the user:
> I need your MongoDB Atlas connection string.
> Get it from: Atlas UI → your cluster → Connect → Drivers
> It looks like: `mongodb+srv://user:pass@cluster.mongodb.net/...`

Ask them to paste it, then write it to `.env`:
```python
python3 -c "
import re, sys
value = sys.argv[1]
with open('.env') as f: c = f.read()
c = re.sub(r'^MONGODB_URI=.*$', 'MONGODB_URI=' + value, c, flags=re.MULTILINE)
with open('.env', 'w') as f: f.write(c)
print('Saved.')
" "<pasted value>"
```

**VOYAGE_API_KEY missing:**
Tell the user:
> I need your Voyage AI API key.
> Get it from: https://dash.voyageai.com/api-keys (free tier is sufficient)

Ask them to paste it, then write it to `.env` the same way.

### 3 — Check domain pack is applied

Run:
```
python3 -c "
from backend.data.demo_records import DEMO_RECORDS
from backend.data.knowledge_base import KNOWLEDGE_BASE
from backend.data.historical_records import HISTORICAL_RECORDS
print(f'{len(DEMO_RECORDS)} demo records, {len(KNOWLEDGE_BASE)} KB items, {len(HISTORICAL_RECORDS)} historical records')
" 2>/dev/null || echo "data_check_failed"
```

If this fails, the domain data files may not be populated. Ask the user if they've run `/init-domain` yet. If not, offer to run it before proceeding.

### 4 — Run setup.py

Run:
```
cd /path/to/repo && backend/.venv/bin/python scripts/setup.py
```

If the venv doesn't exist, tell the user to run `./setup.sh --deps-only` first.

Stream all output to the user. The script takes 1–3 minutes (Voyage AI embedding + waiting for Atlas Vector Search indexes to reach READY state).

### 5 — Report result

On success, tell the user:
```
Setup complete. Start the demo with:
  ./start.sh

Then open http://localhost:5173
```

On failure, show the error output and suggest:
- Check `.env` credentials are correct
- Verify the Atlas cluster is accessible (not paused)
- Check Voyage AI API key has remaining quota
