#!/usr/bin/env python

import sys
from deiis.rabbit import Broadcaster

Broadcaster().broadcast(' '.join(sys.argv[1:]))