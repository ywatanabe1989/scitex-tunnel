# scitex-tunnel

Persistent SSH reverse tunnel for NAT traversal, powered by autossh.

Part of the [SciTeX](https://github.com/ywatanabe1989/scitex-python) ecosystem.

## Overview

A reverse SSH tunnel allows remote access to machines behind firewalls/NAT via a bastion (relay) server.

```
Host (behind NAT) --[reverse tunnel]--> Bastion Server <--[SSH]--> Client
```

## Installation

```bash
pip install scitex-tunnel
```

Or as part of SciTeX:

```bash
pip install scitex[tunnel]
```

### Prerequisites

- `autossh` installed on the host machine (`sudo apt install autossh`)
- SSH key pair for authentication
- A bastion server with SSH access

## Usage

### CLI

```bash
# Set up a persistent reverse tunnel
scitex-tunnel setup -p 2222 -b user@bastion.example.com -s ~/.ssh/id_rsa

# Check tunnel status
scitex-tunnel status
scitex-tunnel status -p 2222

# Remove a tunnel
scitex-tunnel remove -p 2222
```

### Python API

```python
import scitex as stx

# Check availability
print(stx.tunnel.AVAILABLE)  # True

# Set up tunnel
result = stx.tunnel.setup(2222, "user@bastion.example.com", "~/.ssh/id_rsa")

# Check status
result = stx.tunnel.status()
result = stx.tunnel.status(port=2222)

# Remove tunnel
result = stx.tunnel.remove(2222)
```

### Via SciTeX CLI

```bash
scitex tunnel setup -p 2222 -b user@bastion.example.com -s ~/.ssh/id_rsa
scitex tunnel status
scitex tunnel remove -p 2222
```

## How It Works

1. **Setup** creates a systemd service (`autossh-tunnel-<PORT>.service`) that:
   - Uses autossh to maintain a persistent SSH connection
   - Forwards a remote port on the bastion back to localhost:22
   - Auto-restarts on failure

2. **Status** queries systemd for tunnel service state

3. **Remove** stops, disables, and deletes the systemd service

## SSH Key Setup

```bash
# Generate key on host
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# Copy public key to bastion
cat ~/.ssh/id_rsa.pub  # Add to bastion's ~/.ssh/authorized_keys
```

## Troubleshooting

```bash
# Check service status
sudo systemctl status autossh-tunnel-<PORT>.service

# View logs
sudo journalctl -u autossh-tunnel-<PORT>.service -f
```

## Security

- Keep SSH private keys secure (chmod 600)
- Use dedicated keys per tunnel
- Restrict bastion server access

## License

AGPL-3.0
