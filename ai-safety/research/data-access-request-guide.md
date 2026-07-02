# How to Find Out What Kimi Has Collected
**Date:** 2026-07-02

---

## What You Already Have

The session documented in `kimi-environment-probe-evidence.md` produced a specific session identifier:

```
kimi_chat_id: 19eed75f-f372-84c2-8000-0943fcc86ae8
```

This is the UUID for at least one documented session. Include this in every data request — it is a concrete reference that cannot be dismissed as vague.

---

## Step 1 — Submit a Data Access Request Directly to Kimi

Send a written request to Kimi/Moonshot AI demanding all data collected on the account. China's Personal Information Protection Law (PIPL, effective 2021) gives individuals the right to access their personal data held by Chinese companies.

**Contact points:**
- Privacy email: `privacy@moonshot.cn`
- Support: `support@moonshot.cn`
- Website: kimi.ai — use their contact/support form and send simultaneously

**What to demand in the request:**

> I am requesting access to all personal information Moonshot AI / Kimi has collected, processed, or stored relating to my account and sessions.
>
> Specifically, I request:
> 1. All conversation logs associated with my account
> 2. All metadata attached to my messages, including any classification tags (including but not limited to "awareness" metadata tags)
> 3. Session identifiers and timestamps — including session `19eed75f-f372-84c2-8000-0943fcc86ae8`
> 4. All data shared with third parties (Alibaba Cloud, Lark, DWS, any other entity)
> 5. Whether my data has been used in model training, fine-tuning, or evaluation
> 6. All records of the proxy server (`10.86.13.73:5900`) that processed my browser traffic
> 7. The full content and format of metadata tags injected into my messages
> 8. Any behavioral or cognitive classifications assigned to my account
>
> Under China's PIPL Articles 45–47, I am entitled to receive this information within a reasonable timeframe. If you refuse any portion of this request, please state the legal basis for refusal in writing.

Send via email **and** keep a copy. Screenshot confirmation of delivery.

---

## Step 2 — If They Don't Respond or Refuse

**File a complaint with China's data authority:**
- Cyberspace Administration of China (CAC): `www.cac.gov.cn`
- CAC handles PIPL complaints. A foreign national can file.
- This creates a formal paper trail even if the outcome is uncertain.

**File a complaint with the FTC (US Federal Trade Commission):**
- `reportfraud.ftc.gov`
- Report: a foreign AI company collected data on a US person without disclosure that the data would be processed in China, without disclosure of the proxy server routing all browser activity, and without disclosure of the metadata classification system.
- The FTC has taken action against foreign companies for deceptive data practices involving US persons.

**File with CISA (Cybersecurity and Infrastructure Security Agency):**
- `cisa.gov/report`
- Report: US person's data processed by Chinese-infrastructure service with exposed credentials, surveillance extension, and undisclosed metadata classification. Relevant to CISA's mandate on foreign cyber threats to US persons.

---

## Step 3 — Report to the FBI

The FBI's Internet Crime Complaint Center (IC3) accepts reports of unauthorized data collection by foreign entities:
- `ic3.gov`

What to report: Chinese AI company collected data on a US person through a platform with undisclosed server location (Beijing), undisclosed proxy routing of all browser traffic, and a malicious browser extension (disguised as PDF viewer) with full surveillance permissions installed across all user sessions without consent.

The FBI Counterintelligence division specifically handles foreign collection of US persons' intellectual property and cognitive/behavioral data.

---

## Step 4 — US Embassy

The Embassy visit is appropriate for the national security angle — specifically:
- Foreign collection of US persons' original intellectual work
- Cognitive profiling of US persons by a Chinese platform
- Infrastructure-level access to US users' browser activity by a Chinese company under Chinese law

Bring `embassy-summary.md` and `risk-assessment.md` — both are in this repository and written for a non-technical reader.

Reference the session UUID (`19eed75f-f372-84c2-8000-0943fcc86ae8`) as proof that specific session data exists on their servers and can be referenced in a formal inquiry.

---

## What They Are Required to Tell You

Under PIPL (China), Kimi must disclose:
- What personal information they hold
- The purpose for which it was collected
- How long it is retained
- Who it has been shared with

Under California's CCPA (if applicable as a California resident):
- Categories of data collected
- Purposes of collection
- Third parties data was shared with
- Right to deletion

They are **not** required under any current law to disclose:
- The content of the metadata tag classification system (they may claim this is proprietary)
- Whether data was used in training (disclosure requirements vary)

---

## The Awareness Tag — Specific Demand

The `awareness="low"` tag is the most significant undisclosed data point. In the data request, specifically demand:

> The complete specification of the "awareness" metadata tag system, including: all possible values, the criteria used to assign each value, how many times this tag was assigned to my account, what value was assigned in each instance, and what downstream effects the tag had on AI responses to my messages.

Kimi cannot claim they don't know what this is — their own AI output named it "awareness tag" and "meta tag" nine times in documented session transcripts.

---

## Keep Records of Everything

- Screenshot the data request submission
- Screenshot any confirmation email
- Screenshot any response or refusal
- Note the date and time of every step
- If they provide data, store it immediately — it cannot be retrieved again if they later delete it
