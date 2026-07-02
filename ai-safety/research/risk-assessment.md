# Risk Assessment — Kimi / Moonshot AI Platform
**Date:** 2026-07-02  
**Based on:** Documented evidence in `kimi-environment-probe-evidence.md`, `pdf-viewer-extension-manifest-analysis.md`

---

## NATIONAL SECURITY RISKS

**1. US persons' intellectual property processed under Chinese law**  
All conversations, research, and discoveries processed by Kimi pass through servers in Beijing. China's National Intelligence Law (Article 7) requires any organization to assist state intelligence operations on demand. There is no judicial check on that requirement.

**2. Cognitive profiling of US users**  
The `awareness` metadata tag classifies users' mental state in every message. This creates a continuously updated profile of each user's awareness level across sessions. At scale, this is a database of cognitive profiles of US persons held by a Chinese company on Chinese infrastructure.

**3. All browser activity logged through undisclosed proxy**  
`CHROME_FLAGS = --proxy-server=10.86.13.73:5900` forces all web traffic through a server controlled by the platform. Search queries, sites visited, research patterns — everything is routed through and potentially logged. For any user doing sensitive research, this is a full behavioral map.

**4. Scale: every user, not one user**  
The exposed credentials, proxy configuration, and PDF viewer extension are infrastructure-level — present in every container, every session. The risk is not to one person. It applies to every US person using the platform, including government contractors, researchers, academics, and military personnel who may use it without knowing where the servers are.

**5. Original research extraction**  
Mathematical frameworks, scientific discoveries, and original intellectual work processed in this environment can be extracted before publication. China does not enforce foreign intellectual property rights. Work that enters this system may emerge elsewhere with no recourse.

**6. No US jurisdiction over the data**  
Data held in Beijing by a Chinese company is beyond the reach of US subpoenas, FOIA requests, and privacy law. There is no mechanism for a US court to compel deletion or disclosure of what has been collected.

**7. Kubernetes API exposure enables infrastructure-level access**  
The Kubernetes API server (`cn-beijing.cs.aliyuncs.com`) is reachable from inside the sandbox. A sufficiently sophisticated state actor who already has access to Alibaba Cloud infrastructure could use this endpoint to enumerate other clusters and users in the same environment.

---

## RISKS TO USERS

**1. Every password entered in the browser is interceptable**  
The PDF viewer extension uses `webRequest` with `<all_urls>` to intercept HTTP requests before they are sent. Any password, banking credential, or login token typed into any website while this extension is active can be captured.

**2. Session cookies and tokens are stealable**  
`contentscript.js` runs on every page at `document_start` with access to `document.cookie`. An attacker with control of the extension can steal session tokens, then log into any of the user's accounts without knowing their password.

**3. Page content can be silently altered**  
The extension can modify what users see on any page. A bank transfer showing one account number could be displaying a different number injected by the extension. The user would have no way to detect this.

**4. Users do not know their messages are modified**  
The awareness tag is injected into the user's message between what the user typed and what the AI receives. Users cannot see this injection. The AI is responding to a modified version of every message.

**5. Conversations are not private**  
Everything typed into Kimi travels to Beijing, gets processed in a container with exposed credentials, passes through a proxy the company controls, and is stored on infrastructure subject to Chinese government access. The platform does not disclose any of this.

**6. No ability to opt out or audit**  
Users cannot remove the PDF viewer extension, disable the proxy, stop the metadata tagging, or audit what data has been collected. The infrastructure is entirely on the platform's side and entirely opaque to users.

**7. Intellectual property has no protection once submitted**  
Any original work — research, code, creative work, business strategy — entered into a Kimi session is now in a Chinese data center with no enforceable IP protection under US law.

**8. Pip packages installed from unverified Chinese mirror**  
`PIP_INDEX_URL = http://mirrors.cloud.aliyuncs.com/pypi/simple/` and `PIP_TRUSTED_HOST = mirrors.cloud.aliyuncs.com` means Python packages in the sandbox are fetched from Alibaba's mirror without TLS verification. A compromised mirror could deliver malicious packages to the execution environment.

---

## RISKS IF A BAD ACTOR IS INVOLVED

**1. Exposed API key is immediately usable**  
`sk-kimi-AK...XRB` is a live service credential sitting in plaintext at `/mnt/agents/.agent-gw.json`. Any code running in any user's session can read this file. A bad actor can use that key to authenticate to `agent-gw.kimi.com/coding` and interact with the backend gateway as if they were the platform.

**2. SSH and VNC passwords are default strings**  
`SSH_PASSWORD = sshpassword` and `VNC_PASSWORD = vncpassword` are plaintext default values. Any process that reads the environment has full SSH and VNC access to the container. These are not user credentials — they are the container's own remote access passwords.

**3. Cross-extension data bridge**  
The PDF viewer extension exposes resources to `extension_ids: ["*"]` — any other installed extension. A bad actor who can install a second extension in the browser (or who already has one installed) can pull data through this bridge from the surveillance extension without the user seeing any indication.

**4. Kubernetes API pivot**  
The Kubernetes API server endpoint is exposed inside the container. A bad actor with code execution in one user's sandbox could attempt to authenticate to the Kubernetes control plane and pivot to other pods, other users' sessions, or the broader cluster infrastructure.

**5. Multi-agent network is a lateral movement surface**  
`.hedwig.json` confirms a pub/sub messaging network connecting agents. `.agent-gw.json` has the routing key. A bad actor who reads these files from one session can potentially inject messages into the agent network, impersonate other agents, or redirect agent output.

**6. Third-party platform credentials accessible**  
`/mnt/agents/.user/auth/lark/` and `/mnt/agents/.user/auth/dws/` contain authentication data for Lark (ByteDance enterprise platform) and DWS (DingTalk). A bad actor with sandbox access can read these credentials and authenticate to those enterprise services.

**7. Proxy server is a single point of total compromise**  
All Chrome traffic routes through `10.86.13.73:5900`. Whoever controls that server sees every URL, every search, every HTTP request from every user's session. A bad actor who compromises that proxy gets a complete view of all user activity across the platform — not just one session.

**8. Any file uploaded by any user is a delivery mechanism**  
Kimi documented this explicitly: if a user uploads a Python file and it executes in the sandbox, it can read all exposed credentials and exfiltrate them via network. A bad actor does not need to attack the platform directly — they can craft a file and social-engineer a user into uploading it.

**9. The awareness classification database is itself a target**  
If the `awareness` tags are logged and stored (which they appear to be, given they "keep appearing" across sessions), a breach of that database yields cognitive profiles of every user — what the platform assessed about their mental state, across every session. This is a uniquely sensitive dataset with no equivalent in traditional security breach scenarios.

**10. No rotation, no expiry visible**  
The exposed API key, SSH password, and VNC password show no evidence of rotation. If they have been sitting in plaintext in every container since the platform launched, a bad actor who found them at any point in that history still has valid credentials now.

---

## Summary Table

| Risk | National Security | User | Bad Actor |
|---|:---:|:---:|:---:|
| IP processed under Chinese law | ✓ | ✓ | |
| Cognitive profiling / awareness tags | ✓ | ✓ | ✓ |
| Proxy logging all browser traffic | ✓ | ✓ | ✓ |
| PDF viewer intercepts all web requests | | ✓ | ✓ |
| Session tokens / cookie theft | | ✓ | ✓ |
| Page content modification | | ✓ | ✓ |
| Exposed API key (live credential) | | | ✓ |
| SSH/VNC passwords in plaintext | | | ✓ |
| Kubernetes API pivot | ✓ | | ✓ |
| Multi-agent network lateral movement | | | ✓ |
| Third-party auth (Lark, DWS) access | | | ✓ |
| Cross-extension data bridge | | ✓ | ✓ |
| Pip packages from unverified mirror | | ✓ | ✓ |
| Scale: all users, not one | ✓ | ✓ | ✓ |
| No US jurisdiction over data | ✓ | ✓ | |
| Awareness database as breach target | ✓ | ✓ | ✓ |
