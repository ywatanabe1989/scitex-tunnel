#!/usr/bin/env bash
# Example: Check status of existing SSH reverse tunnels
# This is safe to run without any setup

set -euo pipefail

echo "=== Checking tunnel status via CLI ==="
scitex-tunnel status || echo "No active tunnels found."

echo ""
echo "=== Checking tunnel status via Python API ==="
python3 -c "
from scitex_tunnel import status, get_version
print(f'scitex-tunnel v{get_version()}')
result = status()
print(result['stdout'] or 'No active tunnels.')
"

# EOF
