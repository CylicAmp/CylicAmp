# CLASS: AUDIT
"""
The environment status block the owner pasted (owner_work #304, 2026-10-17), read field by field.
The environment id is not copied here; it is in the owner's message in owner_work/messages/2026-10-17.txt.

WHAT THE FIELDS SAY (as stated; "reading" = my reading of the field name, not documented in the block):
  provider cloud                          the environment runs in the cloud
  desired_phase = observed_phase = running   it is running, as asked
  connectivity connected, failure null    connected, no failure reported
  observations_current true               the status is up to date
  spec_revision = observed_spec_revision = 23   the running copy has caught up to configuration revision 23
  network_policy: mode unrestricted, state enforced   outbound network is open (no allow-list) and that policy is applied
  capabilities [], outbound_identities [], runtime_variables [], secrets []   nothing attached: no keys, no credentials, no variables
  source_config_id / source_config_version_id null   not created from a saved configuration (reading)

CHECK OF THE ENVIRONMENT ID: the pasted id has the form ccarenv_b64_<base64>. The base64 decodes to
"ccarenv_5522c116" followed by "!0f$8191ba1f%aa601d80" and two more characters, and the last four
characters pasted ("4MDIINg") do not decode cleanly (they give a control character). "!", "$" and "%" do not
belong in an id made of letters, digits and underscores, so the paste has probably been mistyped or
mis-transcribed. Not settled: which environment this is, and whether it is the one this session runs in
(this session does not expose its environment id).

FALSIFICATION: any assertion failing.
"""
import base64

PREFIX_B64 = "Y2NhcmVudl81NTIyYzExNiEw"          # first 24 characters of the pasted base64
assert base64.b64decode(PREFIX_B64) == b"ccarenv_5522c116!0"
assert base64.b64decode("YTYwMWQ4MDIyNjY=") == b"a601d802266" and base64.b64decode("YTYwMWQ4MDIINg==")[-2:] == b"\x086"

if __name__ == "__main__":
    print("environment status block read; the pasted id decodes to ccarenv_5522c116 plus symbols that do not belong in an id")
