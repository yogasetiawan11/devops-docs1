
# Authentication Methods for Git CLI

When interacting with a remote repository via the Git CLI, authentication is performed using one of two primary mechanisms. These are not separate from the CLI, but the underlying protocols used by Git to securely communicate with remote systems.
## 1. SSH (Typically for Humans)

SSH is based on a public-private key pair, where your machine is registered with the remote system using a public key, and authentication is performed using the corresponding private key.

  -  Authentication model: Asymmetric key-based challenge-response authentication, where the server verifies possession of the private key without it ever being transmitted over the network
  -  User type: Developers and DevOps engineers working interactively, typically mapped to individual user identities on platforms like GitHub
  -  Developer experience: Seamless, no repeated prompts due to SSH agent caching; supports high-frequency operations like push, pull, fetch without re-authentication overhead
   - Security: Strong cryptographic guarantees with no shared secrets; resistant to phishing, credential replay, and man-in-the-middle attacks when host verification is enforced
  -  Access model: Keys are associated with a user account, not just a machine; access is implicitly tied to repository permissions granted to that user
   - Agent support: SSH agents (ssh-agent) securely hold decrypted keys in memory, enabling reuse without exposing private keys or repeatedly entering passphrases
   - Enterprise controls: Keys can be centrally audited, rotated, and revoked; organizations often enforce policies around key types, expiration, and usage

Best Practices (Industry):

 -  Use passphrase-protected SSH keys to protect against local key theft
 -  Prefer modern algorithms (e.g., ed25519 over RSA) for stronger security and performance
 -  Avoid sharing keys across users or systems to maintain accountability
 -  Regularly rotate and remove unused keys to reduce attack surface
 -  Enforce host key verification to prevent MITM attacks
-   Use hardware-backed keys (e.g., security tokens) in high-security environments

## 2. Tokens (Typically for Systems)

Tokens are generated credentials used in place of passwords, designed for controlled, auditable, and programmatic access over HTTPS.

 - Authentication model: Bearer token-based authentication where each request includes a token, and possession of the token is sufficient for access (no additional proof required)
 - User type: CI/CD pipelines, automation tools, scripts, integrations, and non-interactive systems; may represent either a user or a service identity
 - Access control: Fine-grained and explicitly scoped permissions (repository-level, organization-level, or action-specific such as read, write, admin)
 - Security: Can be short-lived, rotated, and revoked; reduces reliance on long-lived static credentials and limits blast radius on compromise
 - Auditability: Every action performed using a token is logged and can be traced back to the issuing identity or system, enabling compliance and monitoring
 - Transport: Works over HTTPS (port 443), making it compatible with restricted networks, proxies, and enterprise firewall policies

Types of Tokens (Common in Industry):

- Personal Access Tokens (PAT)
- Fine-grained tokens (repo-scoped with explicit permissions)
- Service account tokens (non-human identities for automation)
- Short-lived tokens via OIDC federation (modern best practice, issued dynamically at runtime)

Best Practices (Industry):

- Prefer short-lived and dynamically generated tokens over long-lived static credentials
- Follow least privilege principle by granting only the minimum required permissions
- Never hardcode tokens in code, scripts, or repositories
- Store in secure systems (secrets managers, vaults, CI/CD secret stores)
- Rotate frequently and monitor usage for anomalies
- Mask tokens in logs and outputs to prevent accidental exposure

How SSH and Tokens Are Used in Practice

In real-world environments, the choice between SSH and tokens is not fixed. It depends on organizational policies, scale, and security requirements.

In real-world environments, the choice between SSH and tokens is influenced less by developer preference and more by organizational security policies, identity integration, and scalability requirements.

    Developers may use HTTPS with tokens instead of SSH in environments where authentication is integrated with central identity providers (IdPs). In such setups (common in GitHub and GitLab), access is governed by SSO, MFA, and conditional access policies, making token-based authentication easier to enforce, audit, and centrally control than SSH keys.

    While CI/CD systems can use SSH via deploy keys, this approach has both advantages and limitations:

    Advantages:
        Scoped to a single repository, reducing blast radius if compromised
        Simple to configure for isolated automation use cases

    Limitations:
        Limited to repository-level access (no fine-grained, action-level permissions)
        Not tied to a user or centralized identity, making auditing and ownership less clear
        Do not integrate naturally with centralized identity providers (IdPs)
        Often lack strong protection mechanisms (e.g., passphrase usage is uncommon in automation)
        Difficult to manage, rotate, and scale across multiple repositories and pipelines


## Step 1: Generate SSH Keys & Connect to GitHub
Generate SSH Key

Run:
```sh
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/yogaw_github_ed25519

```

This command generates a public-private key pair.

    The private key remains on your machine and must never be shared.
    The public key is added to GitHub, allowing GitHub to recognize your machine.

Let us understand the flags:

    **-t ed25519** Specifies the type of key to generate. Ed25519 is a modern, secure, and recommended algorithm.

    -C Adds a comment to the key. This is simply metadata used for identification and is not limited to email addresses. In practice, developers use their email so platforms like GitHub can associate the key with their account.

    -f Specifies the file name and location of the key. This becomes especially important when managing multiple keys.

    Note: The value passed with -C does not play any role in authentication. It is only used for identification.

Add Key to SSH Agent

In the previous step, we generated an SSH key, which is stored as a private key file on our system. However, SSH does not always know which key to use for authentication with a remote like GitHub, especially when multiple private keys exist on the same machine.

By default, SSH can:

    use keys from the SSH agent (memory)
    fall back to default identity files on disk (e.g., ~/.ssh/id_ed25519, id_rsa)

This creates two practical challenges:

    SSH may try multiple keys sequentially, leading to ambiguity
    Passphrase-protected keys would require repeated manual entry

To solve this, SSH uses a background process called the SSH agent, which loads private keys into memory and makes them available to SSH clients during authentication.
```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/yogaw_github_ed25519
```
    ssh-agent → Starts a background process that manages keys
    ssh-add → Loads your private key into the agent for use during authentication

Verify Loaded Keys

ssh-add -l

    Lists all keys currently loaded in the SSH agent
    Confirms whether your key is available for authentication

Example output:

256 SHA256:abc123... ~/.ssh/yogaw_github_ed25519 (ED25519)

If no keys are loaded:

The agent has no identities.

→ This means your key is not currently in memory, and you need to run ssh-add again
