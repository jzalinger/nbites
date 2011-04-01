import man.motion as motion

"""
Gaits loaded from the gaits/ directory
Each *Gait.py file should be self-sufficient (no cross-dependencies)
"""

from .gaits.FastGait import FAST_GAIT
from .gaits.LabGait import LAB_GAIT
from .gaits.DuckGait import DUCK_GAIT
from .gaits.SlowGait import SLOW_GAIT
from .gaits.ZaphodSlowGait import ZAPHOD_SLOW_GAIT
from .gaits.WebotsGait import WEBOTS_GAIT, WEBOTS_GAIT2
from .gaits.BackwardsGait import BACKWARDS_GAIT
from .gaits.ZmpGait import ZMP_GAIT
 
# disabled / unused gaits
#from .gaits.ComGait import COM_GAIT
#from .gaits.MedGait import MEDIUM_GAIT, MARVIN_MEDIUM_GATE


############# DEFAULT GAIT ASSIGNMENTS ##################

CUR_GAIT = ZMP_GAIT
CUR_DRIBBLE_GAIT = DUCK_GAIT
CUR_BACKWARDS_GAIT = BACKWARDS_GAIT
CUR_SLOW_GAIT = SLOW_GAIT

TRILLIAN_GAIT = CUR_GAIT
ZAPHOD_GAIT   = CUR_GAIT
SLARTI_GAIT   = CUR_GAIT
MARVIN_GAIT   = CUR_GAIT
SPOCK_GAIT    = CUR_GAIT
SCOTTY_GAIT   = CUR_GAIT
DATA_GAIT     = CUR_GAIT
DAX_GAIT      = CUR_GAIT
ANNIKA_GAIT   = CUR_GAIT

TRILLIAN_DRIBBLE_GAIT = CUR_DRIBBLE_GAIT
ZAPHOD_DRIBBLE_GAIT   = CUR_DRIBBLE_GAIT
SLARTI_DRIBBLE_GAIT   = CUR_DRIBBLE_GAIT
MARVIN_DRIBBLE_GAIT   = CUR_DRIBBLE_GAIT
SPOCK_DRIBBLE_GAIT    = CUR_DRIBBLE_GAIT
SCOTTY_DRIBBLE_GAIT   = CUR_DRIBBLE_GAIT
DATA_DRIBBLE_GAIT     = CUR_DRIBBLE_GAIT
DAX_DRIBBLE_GAIT      = CUR_DRIBBLE_GAIT
ANNIKA_DRIBBLE_GAIT   = CUR_DRIBBLE_GAIT

TRILLIAN_BACKWARDS_GAIT = CUR_BACKWARDS_GAIT
ZAPHOD_BACKWARDS_GAIT   = CUR_BACKWARDS_GAIT
SLARTI_BACKWARDS_GAIT   = CUR_BACKWARDS_GAIT
MARVIN_BACKWARDS_GAIT   = CUR_BACKWARDS_GAIT
SPOCK_BACKWARDS_GAIT    = CUR_BACKWARDS_GAIT
SCOTTY_BACKWARDS_GAIT   = CUR_BACKWARDS_GAIT
DATA_BACKWARDS_GAIT     = CUR_BACKWARDS_GAIT
DAX_BACKWARDS_GAIT      = CUR_BACKWARDS_GAIT
ANNIKA_BACKWARDS_GAIT   = CUR_BACKWARDS_GAIT

TRILLIAN_SLOW_GAIT = CUR_SLOW_GAIT
ZAPHOD_SLOW_GAIT   = ZAPHOD_SLOW_GAIT
SLARTI_SLOW_GAIT   = CUR_SLOW_GAIT
MARVIN_SLOW_GAIT   = CUR_SLOW_GAIT
SPOCK_SLOW_GAIT    = CUR_SLOW_GAIT
SCOTTY_SLOW_GAIT   = CUR_SLOW_GAIT
DATA_SLOW_GAIT     = CUR_SLOW_GAIT
DAX_SLOW_GAIT      = CUR_SLOW_GAIT
ANNIKA_SLOW_GAIT   = CUR_SLOW_GAIT


