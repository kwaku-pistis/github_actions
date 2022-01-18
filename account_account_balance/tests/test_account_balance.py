from odoo import fields
from odoo.tests import Form

from .common import TestCommon


class TestAccountAccountBalance(TestCommon):
    def test_account_balance(self):
        payment_form = Form(self.model_account_payment)
        payment_form.date = fields.Date.today()
        payment_form.amount = 200
        payment_form.journal_id = self.rec_bank_journal
        payment_form.partner_type = "customer"
        payment_form.payment_type = "inbound"
        payment_form.journal_id = self.rec_bank_journal
        payment_form.payment_method_id = self.env.ref(
            "account.account_payment_method_manual_in"
        )
        payment_form.destination_account_id = self.account_receivable
        payment = payment_form.save()
        payment.action_post()
        self.assertEqual(payment.state, "posted", "Payment was not posted")
        self.assertEqual(payment.amount, 200, "Payment with wrong amount")

        # Assert if the Payment of 200 registered has been credited to the Account
        # Receivable account
        self.account_receivable.compute_account_balance()
        self.assertEqual(
            self.account_receivable.credit, 200, "Account balance not " "correct"
        )
        self.rec_bank_account.compute_account_balance()
        self.assertEqual(
            self.rec_bank_account.debit, 200, "Account balance not " "correct"
        )
