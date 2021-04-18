# Separates Demographic and Risk Attribution Data and returns a separate dataframe for each

class AttrDemoDataExtract:

    def __init__(self, sdf):
        self.sdf = sdf

    def extract(self):

        demo_df = self.sdf[['ID', 'FirstName', 'MiddleName', 'LastName', 'DOB', 'Sex', 'FavoriteColor', 'ProviderName',
                            'FileDate']].copy()
        quarter_risk_df = self.sdf[['ID', 'AttributedQ1', 'AttributedQ2',
                                    'RiskQ1', 'RiskQ2', 'RiskIncreasedFlag']].copy()

        # print(sdf.head(15))
        return demo_df, quarter_risk_df
