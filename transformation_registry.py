import pandas as pd


class TransformationRegistry:

    @staticmethod
    def PortfolioSummary(df):

        return (
            df.groupby("Portfolio_Code")
              .agg(
                  Holding_Count=("Security", "count"),
                  Total_Weight=("Pct__Assets", "sum")
              )
              .reset_index()
              .sort_values(
                  "Total_Weight",
                  ascending=False
              )
        )

    @staticmethod
    def PortfolioDistribution(df):

        return (
            df.groupby("Portfolio_Code")
              .size()
              .reset_index(
                  name="Count"
              )
        )

    @staticmethod
    def ReportTitle(df):
        return "FMS Holdings Report"

    @staticmethod
    def AsOfDate(df):
        return str(df["As_Of_Date"].iloc[0])

    @staticmethod
    def PortfolioCount(df):
        return str(
            df["Portfolio_Code"].nunique()
        )