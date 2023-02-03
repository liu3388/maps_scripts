# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 22:02:45 2023

@author: tai
"""

import pandas as pd

from fredapi import Fred
fred = Fred(api_key='bdae700e2958f622434c629ac39edee0')
data = fred.get_series('SP500')

#%% private building permits by MSAs. Units, Seasonally adjusted. 
BCN_private = fred.get_series('BOST625BPPRIV')
BCN_private.name = 'Boston-Cambridge-Newtown'

ATL_private = fred.get_series('ATLA013BPPRIVSA')
ATL_private.name = 'Atlanta-Sandy Springs-Alpharetta'








#%% MSA non-farm payroll data, '000 of person, non-seasonally adjusted
BCN_payroll = fred.get_series('SMU25716540000000001')
BCN_payroll.name = 'Boston-Cambridge-Newtown'

