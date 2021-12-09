#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:57:23 2021

@author: haascp
"""

import numpy as np

from mocca.peak.models import IntegratedPeak
from mocca.peak.utils import get_peak_data


def integrate_peak(checked_peak):
    """
    Integrates the peak. Returns an integrated peak with the integral attribute
    set.
    """
    peak_data = get_peak_data(checked_peak)
    integral = np.sum(peak_data).tolist()
    return IntegratedPeak(left=checked_peak.left,
                          right=checked_peak.right,
                          maximum=checked_peak.maximum,
                          dataset=checked_peak.dataset,
                          idx=checked_peak.idx,
                          saturation=checked_peak.saturation,
                          pure=checked_peak.pure,
                          integral=integral)