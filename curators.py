

class DataCurator:

    def __init__(self,cddf,crdf):
        self.cddf = cddf
        self.crdf = crdf

    def curate_demographics(self):
        import numpy as np

        # change middle name to middle initial
        cddf = self.cddf.rename(columns={'MiddleName': 'MI'})
        cddf = cddf.replace(np.nan, '', regex=True)
        cddf['MI'] = cddf['MI'].str[:1]

        # remove time from DOB
        cddf['DOB'] = cddf['DOB'].apply(str)
        cddf['DOB'] = cddf['DOB'].str[:10]

        # change Sex to string and M for 0, F for 1
        cddf['Sex'] = cddf['Sex'].apply(str)
        cddf['Sex'] = cddf['Sex'].apply(lambda x: 'M' if x == 0 else 'F')

        # print(df_new.head(10))
        return cddf

    def curate_risk_attr(self):
        import pandas as pd

        # Transpose the Risk Attributed Flag Information by Quarter
        qrdf_att_col = self.crdf[['ID', 'AttributedQ1', 'AttributedQ2']]
        qrdf_att_t = qrdf_att_col.melt(id_vars=['ID'], var_name='Quarter', value_name='RiskAtt')
        qrdf_att_t['Quarter'] = qrdf_att_t['Quarter'].str.replace('Attributed', '')

        # Transpose the Risk Score Information by Quarter
        qrdf_rsk_col = self.crdf[['ID', 'RiskQ1', 'RiskQ2']]
        qrdf_rsk_t = qrdf_rsk_col.melt(id_vars=['ID'], var_name='Quarter', value_name='RiskScore')
        qrdf_rsk_t['Quarter'] = qrdf_rsk_t['Quarter'].str.replace('Risk', '')

        # Retain the Risk Increased Flag by ID
        qrdf_ri_col = self.crdf[['ID', 'RiskIncreasedFlag']]

        # Risk Attributed and Risk Score Combined
        qrdf_ra_rs = pd.merge(left=qrdf_att_t, right=qrdf_rsk_t, left_on=['ID', 'Quarter'], right_on=['ID', 'Quarter'])

        risk_by_qtr = pd.merge(left=qrdf_ra_rs, right=qrdf_ri_col, how='left', left_on=['ID'], right_on=['ID'])

        return risk_by_qtr
