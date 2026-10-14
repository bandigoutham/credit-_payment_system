import hashlib
from .config import SIMULATION_MODE,SUCCESS_RATE
def simulate_payment(key:str)->tuple[str,str]:
 if SIMULATION_MODE=="random":
  import secrets
  success=secrets.randbelow(10000)/10000 < SUCCESS_RATE
 else:
  success=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)%100 < int(SUCCESS_RATE*100)
 return ("SUCCESS","") if success else ("FAILED","SIMULATED_DECLINE")
