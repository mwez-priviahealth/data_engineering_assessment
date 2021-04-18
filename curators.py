

class DataCurator:

    def __init__(self):
        print('')  # yes this is hacky, I get an indent error if I don't, something to learn here

    def curate_demographics(self, cdf):

        # change middle name to middle initial
        cdf = cdf.rename(columns={'MiddleName': 'MI'})

        # remove time from DOB
        cdf['DOB'] = cdf['DOB'].apply(str)
        cdf['DOB'] = cdf['DOB'].str[:10]

        # change Sex to string and M for 0, F for 1
        # cdf['Sex'] = cdf['Sex'].apply(str)
        cdf['Sex'] = cdf['Sex'].apply(lambda x: 'M' if x == 0 else 'F')

        # print(df_new.head(10))
        return cdf

    def curate_risk_attr(self, cdf):
        import pandas as pd

        # Transpose the Risk Attributed Flag Information by Quarter
        qrdf_att_col = cdf[['ID', 'AttributedQ1', 'AttributedQ2']]
        qrdf_att_t = qrdf_att_col.melt(id_vars=['ID'], var_name='Quarter', value_name='RiskAtt')
        qrdf_att_t['Quarter'] = qrdf_att_t['Quarter'].str.replace('Attributed', '')

        # Transpose the Risk Score Information by Quarter
        qrdf_rsk_col = cdf[['ID', 'RiskQ1', 'RiskQ2']]
        qrdf_rsk_t = qrdf_rsk_col.melt(id_vars=['ID'], var_name='Quarter', value_name='RiskScore')
        qrdf_rsk_t['Quarter'] = qrdf_rsk_t['Quarter'].str.replace('Risk', '')

        # Retain the Risk Increased Flag by ID
        qrdf_ri_col = cdf[['ID', 'RiskIncreasedFlag']]

        # Risk Attributed and Risk Score Combined
        qrdf_ra_rs = pd.merge(left=qrdf_att_t, right=qrdf_rsk_t, left_on=['ID', 'Quarter'], right_on=['ID', 'Quarter'])

        risk_by_qtr = pd.merge(left=qrdf_ra_rs, right=qrdf_ri_col, how='left', left_on=['ID'], right_on=['ID'])

        return risk_by_qtr
