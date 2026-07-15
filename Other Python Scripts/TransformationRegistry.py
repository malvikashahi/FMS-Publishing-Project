class TransformationRegistry:

    @staticmethod
    def PortfolioSummary(df):

        return (
            df.groupby("Portfolio_Code")
              .agg(
                  Holding_Count=("Security","count"),
                  Total_Weight=("Pct__Assets","sum")
              )
              .reset_index()
        )

    @staticmethod
    def PortfolioDistribution(df):

        return (
            df.groupby("Portfolio_Code")
              .size()
              .reset_index(name="Count")
        )