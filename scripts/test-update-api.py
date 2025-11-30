#!/usr/bin/env python3
"""
Test Notion database update API
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

        # Try to update with a simple property
        print("Testing database update...")
        try:
            response = notion.databases.update(
                database_id=command_center_id,
                properties={
                    "指令": {
                        "title": {}
                    }
                }
            )
            print("\n=== Update Response ===")
            print(json.dumps(response, indent=2, ensure_ascii=False))

            # Check if properties were added
            properties = response.get("properties", {})
            print(f"\nProperties count after update: {len(properties)}")

        except Exception as e:
            print(f"\nUpdate error: {str(e)}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
