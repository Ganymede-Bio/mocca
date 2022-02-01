#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:27:44 2022

@author: haascp
"""
import os
import pandas as pd
import datapane as dp


def peaks_to_df(peaks):
    peaks_dict = {'retention_time': [],
                  'offset': [],
                  'compound_id': [],
                  'integral': [],
                  'concentration': [],
                  'file': [],
                  'peak_id': [],
                  'is_saturated': [],
                  'is_pure': [],
                  'istd_keys': [],
                  'istd_concs': [],
                  'is_compound': []}
    for peak in peaks:
        times = peak.dataset.time
        offset_factor = times[1] - times[0]
        peaks_dict['retention_time'].append(times[peak.maximum])
        peaks_dict['offset'].append(peak.offset * offset_factor)
        peaks_dict['file'].append(os.path.basename(peak.dataset.path))
        peaks_dict['peak_id'].append(peak.idx)
        peaks_dict['is_saturated'].append(peak.saturation)
        peaks_dict['is_pure'].append(peak.pure)
        peaks_dict['integral'].append(peak.integral)
        if peak.istd:
            istd_keys = [istd.compound_id for istd in peak.istd]
            istd_concs = [istd.concentration for istd in peak.istd]
            peaks_dict['istd_keys'].append(istd_keys)
            peaks_dict['istd_concs'].append(istd_concs)
        else:
            peaks_dict['istd_keys'].append(None)
            peaks_dict['istd_concs'].append(None)
        peaks_dict['compound_id'].append(peak.compound_id)
        peaks_dict['concentration'].append(peak.concentration)
        peaks_dict['is_compound'].append(peak.is_compound)
    return pd.DataFrame(peaks_dict)


def report_peaks(peak_db, report_path):
    peaks = peak_db.peaks
    peak_df = peaks_to_df(peaks)
    peak_page = dp.Page(
        title="Start page",
        blocks=[
            dp.Group(
                dp.Text("# Peak report"),
                dp.Text("## MOCCA (Multiway Online Chromatographic Chemical Analysis)"),
                columns=2
            ),
            dp.Text("### Table: Peaks in the peak database of the campaign."),
            dp.DataTable(peak_df, label="peak_table")
        ],
    )
    r = dp.Report(
        peak_page
    )
    r.save(path=os.path.join(report_path, "report_peak_db.html"), open=True)
