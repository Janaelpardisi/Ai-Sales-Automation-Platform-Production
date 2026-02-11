"""
Database Migration: Add unsubscribe_token to leads table
"""

import asyncio
import secrets
from sqlalchemy import text
from app.database import get_db, engine


async def add_unsubscribe_token_column():
    """Add unsubscribe_token column to leads table"""
    print("MIGRATION Starting migration: Add unsubscribe_token to leads")
    
    async with engine.begin() as conn:
        # Check if column already exists
        result = await conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM pragma_table_info('leads') 
            WHERE name='unsubscribe_token'
        """))
        row = result.fetchone()
        
        if row and row[0] > 0:
            print("SUCCESS Column 'unsubscribe_token' already exists, skipping...")
            return
        
        # Add the column
        print("NOTE Adding unsubscribe_token column...")
        await conn.execute(text("""
            ALTER TABLE leads 
            ADD COLUMN unsubscribe_token VARCHAR(255)
        """))
        
        # Generate tokens for existing leads
        print("TOKEN Generating tokens for existing leads...")
        result = await conn.execute(text("SELECT id FROM leads WHERE unsubscribe_token IS NULL"))
        lead_ids = [row[0] for row in result.fetchall()]
        
        for lead_id in lead_ids:
            token = secrets.token_urlsafe(32)
            await conn.execute(
                text("UPDATE leads SET unsubscribe_token = :token WHERE id = :id"),
                {"token": token, "id": lead_id}
            )
        
        print(f"SUCCESS Generated tokens for {len(lead_ids)} existing leads")
        
        # Create unique index
        print("STATS Creating unique index on unsubscribe_token...")
        await conn.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_leads_unsubscribe_token 
            ON leads(unsubscribe_token)
        """))
        
    print("COMPLETE Migration completed successfully!")


async def main():
    """Run migration"""
    try:
        await add_unsubscribe_token_column()
    except Exception as e:
        print(f"ERROR Migration failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
