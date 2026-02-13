"""
Test MMB Parser - Movie Magic Budgeting file parser tests
"""
import pytest
import xml.etree.ElementTree as ET
from pathlib import Path


@pytest.fixture
def sample_mmb_file():
    """Load the sample MMB file for testing."""
    file_path = Path(__file__).parent / "fixtures" / "mmb_files" / "atlanta_heist.mmbx"
    return file_path


def test_parse_mmb_budget(sample_mmb_file):
    """Test that we can parse the MMB XML structure."""
    
    # Parse the XML file
    tree = ET.parse(sample_mmb_file)
    root = tree.getroot()
    
    # Check budget version
    assert root.get("version") == "10.0"
    
    # Check header
    header = root.find("Header")
    assert header.find("Title").text == "Atlanta Heist"
    assert header.find("Producer").text == "Example Productions"
    
    # Check total budget
    summary = root.find("Summary")
    total = summary.find("Total").text
    assert float(total) == 2500000
    
    # Check categories exist
    categories = root.find("Categories")
    assert len(categories.findall("Category")) == 5
    
    print("✅ MMB file parsed successfully")


def test_extract_line_items(sample_mmb_file):
    """Test extracting individual line items."""
    
    tree = ET.parse(sample_mmb_file)
    root = tree.getroot()
    
    line_items = []
    
    # Extract all accounts and subaccounts
    for category in root.findall(".//Category"):
        category_name = category.get("name")
        
        for account in category.findall("Account"):
            account_name = account.get("name")
            account_amount = float(account.get("amount", 0))
            
            line_items.append({
                "category": category_name,
                "account": account_name,
                "amount": account_amount,
                "type": "account"
            })
            
            # Get subaccounts
            for sub in account.findall("SubAccount"):
                sub_name = sub.get("name")
                sub_amount = float(sub.get("amount", 0))
                
                line_items.append({
                    "category": category_name,
                    "account": account_name,
                    "subaccount": sub_name,
                    "amount": sub_amount,
                    "type": "subaccount"
                })
    
    # Verify we found all items
    assert len(line_items) > 0
    print(f"✅ Extracted {len(line_items)} line items")
    
    # Check for music scoring (important for demo)
    music_items = [item for item in line_items if "Music" in str(item)]
    assert len(music_items) > 0
