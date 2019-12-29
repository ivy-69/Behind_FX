import pandas as pd
import plotly.graph_objs as go
xls_BOC = pd.ExcelFile('Fx_Rate_BankOfChina.xlsx')
xls_CMB = pd.ExcelFile('Fx_Rate_CMBChina.xlsx')
df_BOC = pd.read_excel(xls_BOC)
df_CMB = pd.read_excel(xls_CMB)
df_BOC = df_BOC[df_BOC['Currency Name'] == 'GBP']
df_CMB = df_CMB[df_CMB['Currency'] == 'GB Pound Sterling']
fig_FX = go.Figure()
fig_FX.add_trace(go.Line(y = df_BOC['Cash Selling Rate'], x = pd.to_datetime(df_BOC['Pub Time']), name='BOC-Selling Rate(GBP)'))
fig_FX.add_trace(go.Line(y = df_CMB['Selling rate'], x = pd.to_datetime(df_CMB['Time']), name='CMB-Selling Rate(GBP)'))
fig_FX.update_layout(
 title="Trend Graph - FX rate",
 xaxis_title="Time",
 yaxis_title="GBP Rate"
)
fig_FX.show()
fig_FX_Spreads = go.Figure()
fig_FX_Spreads.add_trace(go.Line(y = df_BOC['Cash Selling Rate']-df_BOC['Cash Buying Rate'], x = pd.to_datetime(df_BOC['Pub Time']), name='BOC-Bid Rate(GBP)'))
fig_FX_Spreads.add_trace(go.Line(y = df_CMB['Selling rate']-df_CMB['Cash bid'], x = pd.to_datetime(df_CMB['Time']), name='CMB-Bid Rate(GBP)'))
fig_FX_Spreads.update_layout(
 title="Trend Graph - FX spreads rate",
 xaxis_title="Time",
 yaxis_title="Spreads"
)
fig_FX_Spreads.show()
