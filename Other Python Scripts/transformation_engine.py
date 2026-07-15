import pandas as pd


class HoldingsDataObject:
    """
    Loads the holdings file into a pandas DataFrame.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self._load_data()

    def _load_data(self):
        df = pd.read_excel(self.file_path)

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace(" ", "_")
        )

        df["Pct__Assets"] = pd.to_numeric(
            df["Pct__Assets"],
            errors="coerce"
        )

        return df

    def dataframe(self):
        return self.df.copy()


class HoldingsTransformationEngine:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # -----------------------------
    # Generic Filters
    # -----------------------------

    def portfolio(self, portfolio_code):
        return self.df[
            self.df["Portfolio_Code"] == portfolio_code
        ]

    def strategy(self, strategy_name):
        return self.df[
            self.df["Separately_Managed_Equity"] == strategy_name
        ]

    def exclude_cash(self):
        return self.df[
            ~self.df["Security"]
            .astype(str)
            .str.contains(
                "Cash",
                case=False,
                na=False
            )
        ]

    def above_weight(self, weight):
        return self.df[
            self.df["Pct__Assets"] >= weight
        ]

    # -----------------------------
    # Sorting
    # -----------------------------

    def sort_desc(self):
        return self.df.sort_values(
            "Pct__Assets",
            ascending=False
        )

    # -----------------------------
    # Top Holdings
    # -----------------------------

    def top_holdings(self, n=10):
        return (
            self.df
            .sort_values(
                "Pct__Assets",
                ascending=False
            )
            .head(n)
        )

    # -----------------------------
    # Standard FMS Views
    # -----------------------------

    def top10_holdings(self):

        df = self.exclude_cash()

        return (
            df
            .sort_values(
                "Pct__Assets",
                ascending=False
            )
            .head(10)
            [
                [
                    "Security",
                    "Pct__Assets"
                ]
            ]
        )

    def top20_holdings(self):

        df = self.exclude_cash()

        return (
            df
            .sort_values(
                "Pct__Assets",
                ascending=False
            )
            .head(20)
            [
                [
                    "Security",
                    "Pct__Assets"
                ]
            ]
        )

    def portfolio_holdings(self, portfolio_code):

        return (
            self.df[
                self.df["Portfolio_Code"]
                == portfolio_code
            ]
            .sort_values(
                "Pct__Assets",
                ascending=False
            )
        )

    def strategy_holdings(self, strategy_name):

        return (
            self.df[
                self.df["Separately_Managed_Equity"]
                == strategy_name
            ]
            .sort_values(
                "Pct__Assets",
                ascending=False
            )
        )

    def top_portfolio_holdings(
            self,
            portfolio_code,
            top_n=10
    ):

        return (
            self.portfolio_holdings(
                portfolio_code
            )
            .head(top_n)
            [
                [
                    "Security",
                    "Pct__Assets"
                ]
            ]
        )

    def holdings_summary(self):

        return (
            self.df.groupby(
                "Portfolio_Code"
            )["Pct__Assets"]
            .agg(
                Holding_Count="count",
                Total_Weight="sum"
            )
            .reset_index()
        )


if __name__ == "__main__":

    FILE_PATH = "HoldingData.xlsx"

    # -----------------------------
    # Load Holdings File
    # -----------------------------

    holdings_obj = HoldingsDataObject(
        FILE_PATH
    )

    df = holdings_obj.dataframe()

    engine = HoldingsTransformationEngine(
        df
    )

    # -----------------------------
    # Example 1
    # -----------------------------

    top10 = engine.top10_holdings()

    print("\nTOP 10 HOLDINGS")
    print(top10)

    # -----------------------------
    # Example 2
    # -----------------------------

    lcg = engine.top_portfolio_holdings(
        portfolio_code="LCG",
        top_n=10
    )

    print("\nLCG TOP 10")
    print(lcg)

    # -----------------------------
    # Example 3
    # -----------------------------

    sustainable_growth = (
        engine.strategy_holdings(
            "LARGE_CAP_SUSTAINABLE_GROWTH"
        )
    )

    print("\nSUSTAINABLE GROWTH")
    print(
        sustainable_growth.head(10)
    )

    # -----------------------------
    # Example 4
    # -----------------------------

    summary = engine.holdings_summary()

    print("\nPORTFOLIO SUMMARY")
    print(summary)