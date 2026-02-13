"""
MMB Parser Module - Converts MMB files to PilotForge data structures.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class MMBParser:
    """Parse Movie Magic Budgeting files."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = {}
        
    def parse(self) -> Dict[str, Any]:
        """Parse MMB file and return structured data."""
        
        if self.file_path.suffix.lower() == '.mmbx':
            return self._parse_xml()
        elif self.file_path.suffix.lower() == '.csv':
            return self._parse_csv()
        else:
            raise ValueError(f"Unsupported file type: {self.file_path.suffix}")
    
    def _parse_xml(self) -> Dict[str, Any]:
        """Parse .mmbx XML format."""
        
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        # Extract header info
        header = root.find("Header")
        self.data["production"] = {
            "title": header.find("Title").text,
            "producer": header.find("Producer").text,
            "director": header.find("Director").text,
            "shoot_dates": {
                "start": header.find("ShootDates/Start").text,
                "end": header.find("ShootDates/End").text,
                "days": int(header.find("ShootDates/ShootDays").text)
            }
        }
        
        # Extract summary
        summary = root.find("Summary")
        self.data["summary"] = {
            "total": float(summary.find("Total").text),
            "above_line": float(summary.find("AboveLine").text),
            "below_line": float(summary.find("BelowLine").text),
            "post": float(summary.find("Post").text),
            "fringes": float(summary.find("Fringes").text),
            "contingency": float(summary.find("Contingency").text),
            "shoot_weeks": int(summary.find("ShootWeeks").text)
        }
        
        # Extract line items
        self.data["line_items"] = []
        
        for category in root.findall(".//Category"):
            category_name = category.get("name")
            
            for account in category.findall("Account"):
                account_name = account.get("name")
                account_amount = float(account.get("amount", 0))
                
                # Add account level
                self.data["line_items"].append({
                    "category": category_name,
                    "account": account_name,
                    "description": f"{account_name} - Total",
                    "amount": account_amount,
                    "units": account.get("units"),
                    "rate": account.get("rate"),
                    "level": "account"
                })
                
                # Add subaccounts
                for sub in account.findall("SubAccount"):
                    self.data["line_items"].append({
                        "category": category_name,
                        "account": account_name,
                        "description": sub.get("name"),
                        "amount": float(sub.get("amount", 0)),
                        "units": sub.get("units"),
                        "rate": sub.get("rate"),
                        "weeks": sub.get("weeks"),
                        "level": "subaccount"
                    })
        
        return self.data
    
    def _parse_csv(self) -> Dict[str, Any]:
        """Parse CSV export format."""
        
        df = pd.read_csv(self.file_path)
        
        self.data = {
            "production": {
                "title": "Imported Production",
                "producer": "Unknown",
                "director": "Unknown"
            },
            "line_items": df.to_dict('records')
        }
        
        # Calculate summary - handle both 'Amount' and 'amount' column names
        amount_col = 'Amount' if 'Amount' in df.columns else 'amount'
        self.data["summary"] = {
            "total": df[amount_col].sum() if amount_col in df.columns else 0,
            "line_count": len(df)
        }
        
        return self.data
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert parsed data to pandas DataFrame."""
        if "line_items" not in self.data:
            self.parse()
        
        return pd.DataFrame(self.data["line_items"])
    
    def get_eligible_expenses(self, jurisdiction: str) -> pd.DataFrame:
        """Filter for eligible expenses based on jurisdiction rules."""
        df = self.to_dataframe()
        
        # This is where your jurisdiction rules would apply
        # For demo, we'll use Georgia rules
        if jurisdiction == "georgia":
            # Georgia eligible categories
            eligible_mask = df["category"].isin([
                "Below-the-Line", 
                "Post-Production"
            ])
            
            # Add music scoring items
            music_mask = df["description"].str.contains("Scoring", na=False)
            
            # Combine masks to avoid duplicates
            combined_mask = eligible_mask | music_mask
            
            return df[combined_mask]
        
        return df
