import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

raw_data = open('Desafio_VariablesControl_DCH2022_ultimo.csv')
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

benper = pd.DataFrame(bp2, columns=['Fecha',	'Hora',	'Valor_BencenoyPrecursores',	'Archivo'])
c7 = pd.DataFrame(dc2, columns=['Fecha',	'Hora',	'Contenido_C7_Total',	'archivo'])
benper.drop(['Archivo'], axis=1, inplace=True)
c7.drop(['archivo'], axis=1, inplace=True)

data = pd.DataFrame(d2, columns=['TimeStamp', 'tdc_phd.pi_21030', 'tdc_phd.pic_21034', 'tdc_phd.pi_21035', 'tdc_phd.ti_21046', 'tdc_phd.tic_21047', 'tdc_phd.ti_21048', 'tdc_phd.ti_21050', 'tdc_phd.ti_21049', 'tdc_phd.tic_21051', 'tdc_phd.ti_21052', 'tdc_phd.li_21018', 'tdc_phd.lic_21022', 'tdc_phd.fic_21018', 'tdc_phd.fic_24002', 'tdc_phd.fi_21019', 'tdc_phd.fic_22001', 'tdc_phd.fi_21020', 'STMS_DI_21004', 'STMS_LAB_PM_2209-F', 'STMS_PM_2104F', 'STMS_DI_22001', 'STMS_DI_FIC_24002', 'TDC_PHD.FIC_21004', 'TDC_PHD.TI_21004', 'TDC_PHD.FI_21008', 'TDC_PHD.TI_21029', 'TDC_PHD.PIC_22059', 'TDC_PHD.FI_21012', 'TDC_PHD.TI_21036', 'TDC_PHD.PIC_21026', 'TDC_PHD.TI_21054', 'TDC_PHD.TI_22001', 'TDC_PHD.TI_24001'])

data_normalized = raw_data.readlines()
data_normalized = data_normalized[1:]

data_normalized = pd.DataFrame(d2, columns=['TimeStamp','tdc_phd.pi_21030', 'tdc_phd.pic_21034', 'tdc_phd.pi_21035', 'tdc_phd.ti_21046', 'tdc_phd.tic_21047', 'tdc_phd.ti_21048', 'tdc_phd.ti_21050', 'tdc_phd.ti_21049', 'tdc_phd.tic_21051', 'tdc_phd.ti_21052', 'tdc_phd.li_21018', 'tdc_phd.lic_21022', 'tdc_phd.fic_21018', 'tdc_phd.fic_24002', 'tdc_phd.fi_21019', 'tdc_phd.fic_22001', 'tdc_phd.fi_21020', 'STMS_DI_21004', 'STMS_LAB_PM_2209-F', 'STMS_PM_2104F', 'STMS_DI_22001', 'STMS_DI_FIC_24002', 'TDC_PHD.FIC_21004', 'TDC_PHD.TI_21004', 'TDC_PHD.FI_21008', 'TDC_PHD.TI_21029', 'TDC_PHD.PIC_22059', 'TDC_PHD.FI_21012', 'TDC_PHD.TI_21036', 'TDC_PHD.PIC_21026', 'TDC_PHD.TI_21054', 'TDC_PHD.TI_22001', 'TDC_PHD.TI_24001'])
data_normalized.drop(['TimeStamp'], axis=1, inplace=True)

scaler = MinMaxScaler()
scaler.fit(data_normalized)
scaled = scaler.fit_transform(data_normalized)
scaled_df = pd.DataFrame(scaled, columns=data_normalized.columns)

ventana_mediciones = []
valores = np.empty(0)
mediciones = np.empty([4320, 33])
lista_valores = []

for i, pos in c7.iterrows():
    fecha = pos['Fecha']
    hora = pos['Hora']
    tsc7 = fecha + ' ' + hora+'.000'


    indice_coincidencia = data.index[data['TimeStamp']==tsc7].to_list()

    lista_valores.append(pos[2])

    if(len(indice_coincidencia) > 0 ):
        puntero = indice_coincidencia[0]-4320
        mediciones_previas,valor = scaled_df.iloc[puntero:indice_coincidencia[0], 1:], pos[2]

        mediciones_porValor_aux = np.array(mediciones_previas)
        mediciones_porValor = mediciones_porValor_aux.flatten()
        ventana_mediciones.append(mediciones_porValor)

print(len(ventana_mediciones),len(ventana_mediciones[0]))
print(len(lista_valores))

#··················PENDIENTE···················#
#   - Pasar esta lógica a un unico método      #
#       en otro archivo.                       #
#   - Sacar las listas de ventana_mediciones   #
#     y lista_valores a dos archivos csv       #
#   - Realizar lo mismo para el ByP            #
#··············································#

