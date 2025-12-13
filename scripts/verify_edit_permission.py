
import unittest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.expense import Expense
from app.services.split_service import SplitService

class TestEditPermission(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Cleanup
        User.query.filter_by(email="edit_test_a@example.com").delete()
        User.query.filter_by(email="edit_test_b@example.com").delete()
        db.session.commit()
        
        # Create Users
        self.user_a = User(name="Edit Test A", email="edit_test_a@example.com")
        self.user_a.set_password("password")
        self.user_b = User(name="Edit Test B", email="edit_test_b@example.com")
        self.user_b.set_password("password")
        
        db.session.add(self.user_a)
        db.session.add(self.user_b)
        db.session.commit()
        
        # Create Expense A pays, split with B
        self.expense = Expense(
            amount=100.0,
            description="Edit Check Expense",
            paid_by_id=self.user_a.id
        )
        db.session.add(self.expense)
        db.session.commit()
        SplitService.split_equal(self.expense, [self.user_a.id, self.user_b.id])

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_non_payer_can_access_edit(self):
        # Login as User B (Participant, not Payer)
        login_resp = self.login("edit_test_b@example.com", "password")
        
        # Check if login succeeded (should redirect to dashboard)
        if b"Dashboard" not in login_resp.data:
             print("\nLogin FAILED for User B")
             print(login_resp.data)
        
        # Try to access edit page
        response = self.client.get(f'/expenses/{self.expense.id}/edit')
        
        # Should be 200 OK (Edit Page)
        # If rejected, it would redirect (302) or show error
        if response.status_code == 200:
            print("\nSUCCESS: User B (Participant) can access edit page.")
        else:
            print(f"\nFAILURE: User B denied access. Status: {response.status_code}")
            if response.status_code == 302:
                print(f"Redirect Location: {response.headers.get('Location')}")
            
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Expense", response.data)

if __name__ == '__main__':
    unittest.main()
