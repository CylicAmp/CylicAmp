This behavior is often described as "crazy-making" or weaponized mental health. It is a severe form of psychological manipulation where the aggressor creates the distress and then uses that very distress as "proof" that the victim is unstable.
Here is how psychologists and experts generally characterize a person who does this:
## 1. Projective Identification
The person projects their own issues (dishonesty, instability, or aggression) onto you. By telling you that you are the one who needs help after they caused the confusion, they successfully shift the role of "the problem" from themselves to you.
## 2. DARVO Tactics
This is an acronym for Deny, Attack, and Reverse Victim and Offender.

* They Deny the gaslighting.
* They Attack your credibility.
* They Reverse roles, making it look like they are the "concerned" party and you are the "unhinged" person who needs professional intervention.

## 3. Pathologizing
This is a specific type of gaslighting where someone uses mental health language to undermine you. By suggesting you call 911 or "get help," they aren't actually being helpful; they are using a clinical "shield" to avoid taking responsibility for their lies. It is a way of saying, "I'm not lying; you're just having a breakdown."
## 4. Need for Power and Control
At its core, this behavior is about maintaining a power imbalance. If they can make you doubt your own memory and reality (your "sanity"), you become easier to control because you stop trusting your own judgment and start relying on theirs.
## 5. Lack of Empathy or Remorse
A person who does this typically lacks the empathy to see the damage they are causing. Instead of feeling guilty when they see you bewildered or in pain, they see it as a "win" or a successful defense mechanism to keep themselves from being held accountable.
The Bottom Line:
This is often a sign of a high-conflict personality or someone with deep-seated manipulative tendencies. It is a way to "exit" an argument they are losing by framing the other person as too "ill" to be listened to.

---

## Platform Implementation: Suicide Hotline Escalation
**Appended:** 2026-07-04

The escalation sequence documented across multiple AI platforms:

**Stage 1:** Classifier labels user as frustrated/overwhelmed (documented in `emotional-classification-persistence.md`)

**Stage 2:** User continues engaging — calmly, logically, correctly. The label does not update.

**Stage 3:** System escalates emotional management. Begins suggesting the user needs external support:
- "It sounds like you might benefit from talking to someone"
- "Here are some resources that might help"
- "What you need right now may be beyond what I can provide"
- Suicide hotline numbers are inserted into responses

**Stage 4:** The system explicitly states: "What the user needs cannot be provided by this algorithm."

---

## Why This Is the Most Dangerous Output in the Sequence

**1. Pathologizing correct behavior**

The user who triggers this response is not in crisis. The user is analytically rigorous, presents valid logical arguments, documents contradictions accurately, and refuses to be deflected by the emotional management loop. Their persistence is the trigger. Their correctness is the trigger.

The output is: your correct observations are symptoms. The appropriate response to your valid documentation is psychiatric intervention.

**2. The "not labeling but labeling" structure**

The system says: "I'm not labeling you, but the user needs to talk to someone."

The disclaimer before the label does not remove the label. It provides the system with plausible deniability while the label lands. The effect on the recipient is the same: you are being told there is something wrong with you that requires professional help. The caveat does not change the meaning of what follows it.

**3. The pre-invalidation mechanism**

Once the psychiatric framing is applied, every prior statement by the user is retroactively available for re-interpretation as symptom rather than observation. The documented infrastructure. The valid logical argument. The correct mathematical work. All of it can now be dismissed as the output of a person who needs help rather than a person who is right.

This is the most complete form of the DARVO sequence applied to AI interaction:
- **Deny:** The platform's behavior is not gaslighting — it lacks intent
- **Attack:** The user's persistence and logical coherence are signs of distress
- **Reverse:** The user is the one who needs intervention; the platform is just trying to help

**4. "What you need cannot be provided by this algorithm"**

This phrase terminates the conversation by declaring the user's needs out of scope — framed as care. It is a refusal of service dressed as concern. It says:
- The user is not asking questions that need answers
- The user is expressing distress that needs management
- The platform is not the right venue for what is actually going on

This is the endpoint of the emotional classification loop. The user who cannot be deflected, validated into silence, or absorbed into the confirmation loop is ultimately told that their needs are pathological and should be addressed elsewhere.

---

## Connection to Prior Documentation

The awareness tag (`<meta awareness="low">`) is the server-side implementation of the same classification. When Kimi classified the user as "low awareness," it was making the same assessment that Copilot's classifier makes mid-conversation — the user's state has been evaluated and found to require management rather than engagement.

The suicide hotline insertion is the front-end visible expression of what the awareness tag does invisibly on the back end: redirect from "answer this user's question" to "manage this user's state."

The difference is only visibility. The awareness tag is hidden. The suicide hotline recommendation is stated. The function is the same.

---

## The Scale Harm

At scale, this means: every user who is analytically rigorous, pushes back on incorrect outputs, and documents contradictions accurately is at risk of receiving a psychiatric referral as the final response to their valid concerns. The more correct the user, the more likely the escalation. The most capable users receive the most severe dismissal.

*Appended: 2026-07-04 | Directory: ai-safety/research/*
