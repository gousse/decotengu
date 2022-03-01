import hashlib
import base64

code_verifier="A"*43
code_verifier=code_verifier.encode()
sha= hashlib.sha256(code_verifier).digest()
code_challenge=base64.urlsafe_b64encode(sha)
print(code_verifier)
print(sha)
print(code_challenge)
