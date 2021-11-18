"""
verify.py
"""
from configs import App_Configs

def verify(token):
    print(App_Configs.authorization)
    if token is None or 'Bearer' not in token:
        verified = False
    elif token[7:] != App_Configs.authorization:
        verified = False
    else:
        verified = True

    return verified
