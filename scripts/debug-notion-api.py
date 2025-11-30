#!/usr/bin/env python3
"""
Debug script to investigate Notion API behavior
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

def main():
    notion_api_key = os.getenv("NOTION_API_KEY")
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")

    if not all([notion_api_key, command_center_id]):
        print("Missing credentials")
        sys.exit(1)

    try:
        from notion_client import Client

        notion = Client(auth=notion_api_key)

        # Retrieve the database
        print("Retrieving database...")
        db = notion.databases.retrieve(database_id=command_center_id)

        # Print the full response
        print("\n=== Full Database Response ===")
        print(json.dumps(db, indent=2, ensure_ascii=False))

        # Check properties
        properties = db.get("properties", {})
        print(f"\n=== Properties Count: {len(properties)} ===")
        for prop_name, prop_data in properties.items():
            print(f"- {prop_name}: {prop_data.get('type', 'unknown')}")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
