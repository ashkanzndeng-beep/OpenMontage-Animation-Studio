# Google Flow Integration — User Sign-in Boundary

## Purpose
Use Google Flow as a future video production surface while keeping credentials
and browser sessions in the user's own authorized account.

## Current state
**Not connected.** The existence of a Google GenAI/Veo/Gemini Omni provider
adapter in OpenMontage does not imply an official Google Flow web-UI API.
Never equate API access with a logged-in Flow browser session.

## Handoff checklist (when video generation needs Google Flow)
1. Tell the user why Flow is needed, which shot/asset, expected model/cost,
   and what the assistant can actually do in the active execution mode.
2. User opens Google Flow in a browser and signs into their own Google account;
   user handles 2FA, consent, billing and any legal/account permissions.
3. In ChatGPT Work or an explicitly authorized computer-use/browser session,
   connect/select that signed-in browser tab, if supported. Chat-only GitHub
   access does not grant browser control.
4. Inspect Flow UI capabilities and terms at that time; test with a **single**
   approved sample before promising end-to-end automation.
5. Save generation results and provenance in the local project artifacts;
   keep passwords, session cookies, private keys and tokens out of GitHub.
6. If browser control is unavailable, prepare a copy/paste production pack:
   English prompt, reference frames, camera, timings and QA criteria.
7. Never attempt to bypass rate limits, access controls, CAPTCHAs, payment or
   approval steps; never claim an unverified render was generated.

No browser automation, Google account access, or paid call is performed in
this bootstrap commit.
