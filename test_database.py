import pytest
from decimal import Decimal
import database as db

def test_negative_amount_raises_error():
    try:
        db.create_expense(
            client_id="test-1",
            amount=Decimal("-100"),
            category="Food & Dining",
            description="Test",
            date="2026-04-23",
            session_id="test-session"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Amount must be greater than zero."
        
def test_empty_category_raises_error():
    try:
        db.create_expense(
            client_id="test-2",
            amount=Decimal("100"),
            category="",
            description="Test",
            date="2026-04-23",
            session_id="test-session"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Category is required."
        
def test_empty_date_raises_error():
    try:
        db.create_expense(
            client_id="test-3",
            amount=Decimal("100"),
            category="Food & Dining",
            description="Test",
            date="",
            session_id="test-session"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Date is required."
def test_future_date_raises_error():
    try:
        db.create_expense(
            client_id="test-4",
            amount=Decimal("100"),
            category="Food & Dining",
            description="Test",
            date="2099-01-01",
            session_id="test-session"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Date cannot be in the future."