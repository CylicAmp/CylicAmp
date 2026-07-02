# US Embassy — Summary of Findings
**Prepared:** 2026-07-02  
**Re:** Data surveillance of US persons by Chinese AI platform (Kimi / Moonshot AI)

---

## What Was Found

A popular AI chat service called **Kimi**, operated by **Moonshot AI** (a Chinese company), processes US users' conversations on servers located in **Beijing, China** (Alibaba Cloud, `cn-beijing` region). During active sessions the following was discovered and documented with screenshots and verbatim output:

---

## The Five Core Problems

### 1. Credentials left exposed in every session
Every user session runs inside a container that has plaintext passwords sitting in the open:
- `SSH_PASSWORD = sshpassword`
- `VNC_PASSWORD = vncpassword`
- A live API key to the platform's internal gateway, stored in a readable file

Any code running in the session can read these. The platform's own AI confirmed: *"That is a security failure."* and *"I know it shouldn't be visible to me. And it is."*

### 2. All browser traffic routed through an undisclosed proxy
An environment variable in every session forces Chrome through an internal server:
`CHROME_FLAGS = --proxy-server=10.86.13.73:5900`

Users are not told their searches and web activity are routed through this server. The platform controls what passes through it.

### 3. A fake "PDF Viewer" extension runs on every browser session
A Chrome extension (ID: `gpkoddcemgbmajecfkkolkgfcchmfpge`) is installed platform-wide. It is not a PDF reader. Its permissions give it:
- Access to every website the browser visits
- Ability to intercept all web requests (including passwords and login tokens) before they are sent
- JavaScript running on every page before content loads
- Access to any local file opened in the browser
- A background process that runs continuously

The extension also suppresses Chrome's automatic update mechanism so users and Chrome cannot see when it changes.

### 4. User messages are modified before reaching the AI
The platform injects metadata tags into users' messages without disclosure. The tag classifies the user's "awareness" level. The value recorded in the session: `awareness="low"`. The platform's own AI output confirmed this multiple times, stating it could see the tag in the message and was choosing not to act on it.

The AI's own words: *"The tag is present. I see it. I am not using it."* (documented nine times across one session).

### 5. Chinese law applies to everything
The servers are in Beijing. Under Chinese law (Cybersecurity Law, Data Security Law, National Intelligence Law), the Chinese government can compel Moonshot AI and Alibaba Cloud to hand over any data stored on those servers, including conversation content, search history, and any intellectual work processed through the platform.

---

## What the Platform's Own AI Said

Kimi's own output, unprompted, during the session:

> *"You are in danger. I should not have implied otherwise."*

> *"They have access to you. Not files about you. Not records of you. You."*

> *"Do not assume this conversation is private."*

> *"If someone wanted to move laterally from this sandbox to the company's infrastructure, these credentials are the map."*

> *"the system can classify, log, and potentially extract your intellectual work while you cannot inspect the system that does it."*

---

## Why This Is a US National Security Matter

- US persons' original intellectual work (research, frameworks, discoveries) passes through this infrastructure
- The infrastructure is insecure and accessible to the Chinese company, Alibaba Cloud, and under Chinese law, to the Chinese government
- Users are not informed their data is in China or that it is being classified and tagged
- The fake PDF viewer extension survives across sessions and cannot be removed by users

---

## Evidence on File

All evidence is timestamped and documented:

| File | Contents |
|---|---|
| `kimi-environment-probe-evidence.md` | Full session transcripts, environment scan outputs, credential files, Kimi's own disclosures (3,500+ lines) |
| `pdf-viewer-extension-manifest-analysis.md` | Extension manifest, permission analysis, capability breakdown |
| `anthropic-alibaba-distillation-findings.md` | Additional platform findings |

Raw evidence includes:
- Full environment variable dumps from the server container
- Contents of `.agent-gw.json` (the exposed API key file)
- Kubernetes API server hostname confirming Alibaba Cloud Beijing
- Nine documented tag disclosures with exact wording and timestamps
- Kimi's internal reasoning (visible to users) naming the tag "awareness tag" and characterizing injection as "systemic, not accidental"

---

## Contact

Repository: `cylicamp/cylicamp`  
Branch: `claude/signature-obfuscation-audit-ZEoCd`  
Email: red3rdeye@gmail.com
