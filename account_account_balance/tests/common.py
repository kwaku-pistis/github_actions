from odoo.tests import tagged
from odoo.tests.common import SavepointCase


@tagged("-at_install", "post_install")
class TestCommon(SavepointCase):
    """Shared base class for 'account.account' test cases.
    This bootstraps most of the records needed by the 'account.account' test cases.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Models
        cls.model_account_payment = cls.env["account.payment"]
        cls.model_account_journal = cls.env["account.journal"]
        cls.model_account_account = cls.env["account.account"]

        cls.rec_bank_account = cls.model_account_account.create(
            {
                "name": "Bank Account",
                "code": "100234",
                "user_type_id": cls.env.ref("account.data_account_type_liquidity").id,
            }
        )

        cls.account_receivable = cls.model_account_account.create(
            {
                "code": "10200",
                "name": "Account Receivable",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )

        cls.rec_bank_journal = cls.model_account_journal.create(
            {
                "name": "Bank Journal",
                "code": "BNK JNRL",
                "type": "bank",
                "default_account_id": cls.rec_bank_account.id,
                "suspense_account_id": cls.rec_bank_account.id,
                "payment_debit_account_id": cls.rec_bank_account.id,
                "payment_credit_account_id": cls.rec_bank_account.id,
            }
        )
