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

CHECK OF THE ENVIRONMENT ID (corrected 2026-10-17: the first version guessed that the symbols were a mistyping):
  The pasted id has the form ccarenv_b64_<base64>. Decoded as pasted, the base64 gives "ccarenv_5522c116" then
  "!0f$8191ba1f%aa601d80" and a last stretch that does not decode cleanly: the pasted ending "4MDIINg"
  gives a control character. With "4MDI2Ng" instead ("I" read for "2" -- typo) the ending decodes to the digits
  "266". The "!", "$" and "%" decode from the pasted base64 itself. Whether they belong to the id's real format
  or come from a copying error: NOT SETTLED -- the format of this id is not known to me. Also not settled:
  which environment this is, and whether it is the one this session runs in (this session exposes no
  environment-id variable; checked by listing variable names, not values).

FALSIFICATION: any assertion failing.
"""
import base64

PREFIX_B64 = "Y2NhcmVudl81NTIyYzExNiEw"          # first 24 characters of the pasted base64
assert base64.b64decode(PREFIX_B64) == b"ccarenv_5522c116!0"
assert base64.b64decode("YTYwMWQ4MDI2Ng==") == b"a601d80266"                 # ending with "I2Ng": clean digits
assert base64.b64decode("YTYwMWQ4MDIINg==")[-2:] == b"\x086"                 # ending as pasted, "IINg": control character

if __name__ == "__main__":
    print("environment status block read; the id decodes to ccarenv_5522c116 plus symbols; ending decodes cleanly only with I2Ng; format not settled")
