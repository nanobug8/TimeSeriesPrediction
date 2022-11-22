import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import csv

raw_data = open('Desafio_VariablesControl_DCH2022.csv')
c7_data = open("Desafio_Contenido_C7_Total_11-2017_09-2021.csv")
byp_data = open("Desafio_BencenoyPrecursoresTotal_11-2017_09-2021.csv")

df = raw_data.readlines()
df = df[1:]

c7_data = c7_data.readlines()
c7_data = c7_data[1:]

byp_data = byp_data.readlines()
byp_data = byp_data[1:]

d1 = []
for i in df:
    d1.append(i.replace("\n", ""))

dc1 = []
for i in c7_data:
    dc1.append(i.replace("\n", ""))

bp1 = []
for i in byp_data:
    bp1.append(i.replace("\n", ""))

d2 = []
for i in d1:
    x = i.split(';')
    d2.append(x)

dc2 = []
for i in dc1:
    x = i.split(',')
    dc2.append(x)

bp2 = []
for i in bp1:
    x = i.split(',')
    bp2.append(x)

benper = pd.DataFrame(bp2, columns=['_date', '_time', 'Valor_BencenoyPrecursores', 'Archivo'])
c7 = pd.DataFrame(dc2, columns=['_date', '_time', 'Contenido_C7_Total', 'archivo'])
benper.drop(['Archivo'], axis=1, inplace=True)
c7.drop(['archivo'], axis=1, inplace=True)

data = pd.DataFrame(d2, columns=['TimeStamp', 'tdc_phd.pi_21030', 'tdc_phd.pic_21034', 'tdc_phd.pi_21035',
                                 'tdc_phd.ti_21046', 'tdc_phd.tic_21047', 'tdc_phd.ti_21048', 'tdc_phd.ti_21050',
                                 'tdc_phd.ti_21049', 'tdc_phd.tic_21051', 'tdc_phd.ti_21052', 'tdc_phd.li_21018',
                                 'tdc_phd.lic_21022', 'tdc_phd.fic_21018', 'tdc_phd.fic_24002', 'tdc_phd.fi_21019',
                                 'tdc_phd.fic_22001', 'tdc_phd.fi_21020', 'STMS_DI_21004', 'STMS_LAB_PM_2209-F',
                                 'STMS_PM_2104F', 'STMS_DI_22001', 'STMS_DI_FIC_24002', 'TDC_PHD.FIC_21004',
                                 'TDC_PHD.TI_21004', 'TDC_PHD.FI_21008', 'TDC_PHD.TI_21029', 'TDC_PHD.PIC_22059',
                                 'TDC_PHD.FI_21012', 'TDC_PHD.TI_21036', 'TDC_PHD.PIC_21026', 'TDC_PHD.TI_21054',
                                 'TDC_PHD.TI_22001', 'TDC_PHD.TI_24001'])

data_normalized = raw_data.readlines()
data_normalized = data_normalized[1:]

data_normalized = pd.DataFrame(d2, columns=['TimeStamp', 'tdc_phd.pi_21030', 'tdc_phd.pic_21034', 'tdc_phd.pi_21035',
                                            'tdc_phd.ti_21046', 'tdc_phd.tic_21047', 'tdc_phd.ti_21048',
                                            'tdc_phd.ti_21050', 'tdc_phd.ti_21049', 'tdc_phd.tic_21051',
                                            'tdc_phd.ti_21052', 'tdc_phd.li_21018', 'tdc_phd.lic_21022',
                                            'tdc_phd.fic_21018', 'tdc_phd.fic_24002', 'tdc_phd.fi_21019',
                                            'tdc_phd.fic_22001', 'tdc_phd.fi_21020', 'STMS_DI_21004',
                                            'STMS_LAB_PM_2209-F', 'STMS_PM_2104F', 'STMS_DI_22001', 'STMS_DI_FIC_24002',
                                            'TDC_PHD.FIC_21004', 'TDC_PHD.TI_21004', 'TDC_PHD.FI_21008',
                                            'TDC_PHD.TI_21029', 'TDC_PHD.PIC_22059', 'TDC_PHD.FI_21012',
                                            'TDC_PHD.TI_21036', 'TDC_PHD.PIC_21026', 'TDC_PHD.TI_21054',
                                            'TDC_PHD.TI_22001', 'TDC_PHD.TI_24001'])
data_normalized.drop(['TimeStamp'], axis=1, inplace=True)

scaler = MinMaxScaler()
scaler.fit(data_normalized)
scaled = scaler.fit_transform(data_normalized)
scaled_df = pd.DataFrame(scaled, columns=data_normalized.columns)

window_measures_AUXC7 = []
window_measures_C7 = []
window_measures_2_C7 = []
list_values_C7 = []

window_measures_AUXBP = []
window_measures_BP = []
window_measures_2_BP = []
list_values_BP = []

values = np.empty(0)
measures = np.empty([4320, 33])

######  benzene and precursors WORKLOAD ########

for i, pos in benper.iterrows():
    _date = pos['_date']
    _time = pos['_time']
    tsbenper = _date + ' ' + _time + '.000'

    index_match = data.index[data['TimeStamp'] == tsbenper].to_list()

    list_values_BP.append(pos[2])

    if len(index_match) > 0:
        pointer = index_match[0] - 4320
        measures_previous, valor = scaled_df.iloc[pointer:index_match[0]], pos[2]

        measures_perValue_aux = np.array(measures_previous)
        measures_perValue = measures_perValue_aux.flatten()
        window_measures_AUXBP.append(measures_perValue)

for med_BP in window_measures_AUXBP:
    window_measures_BP.append(med_BP[0::2])
    window_measures_2_BP.append(med_BP[1::2])

print(len(window_measures_BP), len(window_measures_BP[0]))
print(len(window_measures_2_BP), len(window_measures_2_BP[0]))
print(len(list_values_BP))

######  C7+ WORKLOAD ########

for i, pos in c7.iterrows():
    _date = pos['_date']
    _time = pos['_time']
    tsc7 = _date + ' ' + _time + '.000'

    index_match = data.index[data['TimeStamp'] == tsc7].to_list()

    list_values_C7.append(pos[2])

    if len(index_match) > 0:
        pointer = index_match[0] - 4320
        measures_previous, valor = scaled_df.iloc[pointer:index_match[0]], pos[2]

        measures_perValue_aux = np.array(measures_previous)
        measures_perValue = measures_perValue_aux.flatten()
        window_measures_AUXC7.append(measures_perValue)

for med in window_measures_AUXC7:
    window_measures_C7.append(med[0::2])
    window_measures_2_C7.append(med[1::2])

print(len(window_measures_C7), len(window_measures_C7[0]))
print(len(window_measures_2_C7), len(window_measures_2_C7[0]))
print(len(list_values_C7))

#### write csv outputs for c7 measures

output_C7_measures_pairs = open('output_C7_measures_pairs.csv', 'w+', newline ='')
with output_C7_measures_pairs:
    write = csv.writer(output_C7_measures_pairs)
    write.writerows(window_measures_C7)

output_C7_measures_odd = open('output_C7_measures_odd.csv', 'w+', newline ='')
with output_C7_measures_odd:
    write = csv.writer(output_C7_measures_odd)
    write.writerows(window_measures_2_C7)

output_values_C7 = open('output_values_C7.csv', 'w+', newline ='')
with output_values_C7:
    write = csv.writer(output_values_C7)
    write.writerows(list_values_C7)


#### write csv outputs for benzene and precursors measures

output_BP_measures_pairs = open('output_BP_measures_pairs.csv', 'w+', newline ='')
with output_BP_measures_pairs:
    write = csv.writer(output_BP_measures_pairs)
    write.writerows(window_measures_BP)

output_BP_measures_odd = open('output_BP_measures_odd.csv', 'w+', newline ='')
with output_BP_measures_odd:
    write = csv.writer(output_BP_measures_odd)
    write.writerows(window_measures_2_BP)

output_values_BP = open('output_values_BP.csv', 'w+', newline ='')
with output_values_BP:
    write = csv.writer(output_values_BP)
    write.writerows(list_values_BP)

