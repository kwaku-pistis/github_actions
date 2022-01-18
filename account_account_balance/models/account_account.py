from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    debit = fields.Float(string="Debit", compute="_compute_account_balance")
    credit = fields.Float(string="Credit", compute="_compute_account_balance")
    balance = fields.Float(string="Balance", compute="_compute_account_balance")

    def _compute_account_balance(self):
        for rec in self:
            sql = """
                SELECT SUM(COALESCE(debit,0)) debit, SUM(COALESCE(credit,0)) credit,
                SUM(COALESCE(debit,0)-COALESCE(credit,0)) balance
                FROM account_move_line aml,account_move am
                WHERE aml.move_id=am.id
                AND account_id=%s
                AND am.state='posted'
            """
            self._cr.execute(sql, (rec.id,))
            r = self._cr.fetchone()
            rec.debit = r[0]
            rec.credit = r[1]
            rec.balance = r[2]
