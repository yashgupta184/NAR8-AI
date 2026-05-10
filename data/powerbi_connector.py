# data/powerbi_connector.py
"""
NAR8 AI — Power BI REST API Connector

Handles two modes:
  1. MOCK MODE (USE_MOCK_DATA=true): Returns generated fake data
  2. LIVE MODE (USE_MOCK_DATA=false): Authenticates with Azure AD
     and executes a DAX query against a real Power BI semantic model

Authentication uses OAuth 2.0 Client Credentials Flow:
  - Your Azure App (client_id + client_secret) acts as the identity
  - You exchange these credentials for a Bearer token
  - That token is attached to every Power BI API request
"""
import requests
import pandas as pd
from config.settings import Config
from data.mock_sales_data import generate_mock_sales_data


class PowerBIConnector:
    """
    Abstracts the data source behind a clean interface.
    All other modules call fetch_weekly_sales() and do not
    care whether it came from the API or mock generator.
    """

    def __init__(self):
        self.config = Config()
        self._access_token: str = ""

    def _get_access_token(self) -> str:
        """
        Authenticates with Azure Active Directory using the
        Client Credentials OAuth 2.0 flow and returns a Bearer token.

        This is a machine-to-machine authentication pattern —
        no human login required. Your app proves its identity
        using client_id + client_secret.
        """
        try:
            import msal
        except ImportError:
            raise ImportError("Run: pip install msal")

        authority = f"https://login.microsoftonline.com/{self.config.POWERBI_TENANT_ID}"

        app = msal.ConfidentialClientApplication(
            client_id=self.config.POWERBI_CLIENT_ID,
            client_credential=self.config.POWERBI_CLIENT_SECRET,
            authority=authority,
        )

        result = app.acquire_token_for_client(
            scopes=["https://analysis.windows.net/powerbi/api/.default"]
        )

        if "access_token" not in result:
            error = result.get("error_description", "Unknown error")
            raise ValueError(f"Power BI authentication failed: {error}")

        print("✅ Power BI authentication successful")
        return result["access_token"]

    def _execute_dax_query(self, dax_query: str) -> pd.DataFrame:
        """
        Sends a DAX query to the Power BI Execute Queries API endpoint.

        DAX (Data Analysis Expressions) is Power BI's formula language.
        The Execute Queries API accepts a DAX query string and returns
        results as JSON, which we convert to a pandas DataFrame.

        API Endpoint:
          POST /v1.0/myorg/groups/{workspaceId}/datasets/{datasetId}/executeQueries

        Args:
            dax_query: Valid DAX query string

        Returns:
            pandas DataFrame with query results
        """
        if not self._access_token:
            self._access_token = self._get_access_token()

        url = (
            f"https://api.powerbi.com/v1.0/myorg/groups/"
            f"{self.config.POWERBI_WORKSPACE_ID}/datasets/"
            f"{self.config.POWERBI_DATASET_ID}/executeQueries"
        )

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "queries": [{"query": dax_query}],
            "serializerSettings": {"includeNulls": True},
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 401:
            # Token may have expired — refresh and retry once
            self._access_token = self._get_access_token()
            headers["Authorization"] = f"Bearer {self._access_token}"
            response = requests.post(url, headers=headers, json=payload, timeout=30)

        response.raise_for_status()

        data = response.json()
        rows = data["results"][0]["tables"][0]["rows"]
        return pd.DataFrame(rows)

    def _parse_powerbi_response(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalizes the raw Power BI API response into the same
        column structure as the mock data generator.

        Power BI returns column names like '[Table].[ColumnName]' —
        we clean and rename them to match our internal schema.
        """
        # Power BI prefixes column names with the table/measure name
        # Adapt these renames to match your actual semantic model column names
        column_map = {
            "[Date].[WeekStartDate]":            "week_start_date",
            "[Product].[Category]":              "category",
            "[Sales Territory].[Region]":        "region",
            "[Measures].[Sales Amount]":          "sales_amount",
            "[Measures].[Units Sold]":            "units_sold",
            "[Measures].[Returns Amount]":        "returns_amount",
        }
        df = df.rename(columns=column_map)
        df["week_start_date"] = pd.to_datetime(df["week_start_date"])
        df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce").fillna(0)
        df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce").fillna(0).astype(int)
        df["returns_amount"] = pd.to_numeric(df["returns_amount"], errors="coerce").fillna(0)

        # Derive avg_order_value if not already present
        if "avg_order_value" not in df.columns:
            df["avg_order_value"] = (
                df["sales_amount"] / df["units_sold"].replace(0, 1)
            ).round(2)

        # Add week number
        min_date = df["week_start_date"].min()
        df["week_number"] = ((df["week_start_date"] - min_date).dt.days // 7 + 1)

        return df

    def fetch_weekly_sales(self, weeks: int = None) -> pd.DataFrame:
        """
        Main public method — fetches weekly sales data.

        In MOCK MODE: returns generated data instantly (no internet needed)
        In LIVE MODE: authenticates with Azure and queries Power BI

        Args:
            weeks: Number of weeks to fetch (default from Config)

        Returns:
            pandas DataFrame with standardized columns
        """
        if weeks is None:
            weeks = Config.WEEKS_OF_DATA

        if self.config.USE_MOCK_DATA:
            print(f"INFO: NAR8 AI running in MOCK DATA mode")
            print(f"      (Set USE_MOCK_DATA=false in .env for real Power BI)")
            return generate_mock_sales_data(weeks=weeks)

        print("Connecting to Power BI REST API...")

        # This DAX query retrieves weekly aggregated sales from the semantic model
        # Adapt the table/column names to match your actual Power BI model
        dax_query = f"""
        EVALUATE
        SUMMARIZECOLUMNS (
            'Date'[WeekStartDate],
            'Product'[Category],
            'Sales Territory'[Region],
            "Sales Amount",   [Total Sales],
            "Units Sold",     [Total Units],
            "Returns Amount", [Total Returns]
        )
        ORDER BY 'Date'[WeekStartDate] ASC
        """

        raw_df = self._execute_dax_query(dax_query)
        df = self._parse_powerbi_response(raw_df)

        print(f"Fetched {len(df)} rows from Power BI")
        return df
