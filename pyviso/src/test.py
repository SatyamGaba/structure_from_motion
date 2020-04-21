import pyximport; pyximport.install()

import pyviso2 as pv

params = pv.Parameters(f=645.24, cu=635.96, cv=194.13, baseline=0.5707)
vo = PyVisualOdometryStereo(params)

