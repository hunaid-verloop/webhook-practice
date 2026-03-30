from common.webhooker import WebHooker
from common.datastructures import card, quick_reply, postback, url, action


class Bot(WebHooker):

    def Get_Supported_Operators(self, *args, visitor, variables, **kwargs):
        operators = [
            quick_reply(title="Vodafone",
                        action=action(operator="vodafone",
                                      next_block="Get_Plans_Wait")),
            quick_reply(title="Airtel",
                        action=action(operator="airtel",
                                      next_block="Get_Plans_Wait")),
            quick_reply(title="Jio",
                        action=action(operator="jio",
                                      next_block="Get_Plans_Wait"))
        ]
        self.next_block(name="Show_Operators")
        self.export(OperatorList=operators)

    def validate_operator(self, *args, visitor, variables, **kwargs):
        if not self._is_valid_op(variables.get("operator")):
            self.next_block(name="Invalid_Operator")

    def Get_Plans(self, *args, visitor, variables, **kwargs):
        if not self._is_valid_op(variables.get("operator")):
            self.next_block(name="Invalid_Operator")
            self.export(PlanList=[])
            return

        plans = [
            card(
                title="Data 1 GB (28 days)",
                subtitle="Rs. 100",
                buttons=[
                    postback(
                        title="Select",
                        action=action(amount=555, next_block='Do_Recharge')
                    ),
                    url(title="Know More", url="https://verloop.io")
                ]
            ),
            card(
                title="Full Talk time (84 days)",
                subtitle="Rs. 555",
                buttons=[
                    postback(
                        title="Select",
                        action=action(amount=555, next_block='Do_Recharge')
                    ),
                    url(title="Know More", url="https://verloop.io")
                ]
            )
        ]
        self.next_block(name="Show_Plans_Text")
        self.export(PlanList=plans)

    def Get_Payment_Link(self, *args, visitor, variables, **kwargs):
        if not self._is_valid_op(variables.get("operator")):
            self.next_block(name="Invalid_Operator")
            self.export(PaymentOptions=[])
            return
        amount = variables.get("amount", {}).get("parsed_value", None)
        recharge_number = variables.get("rechargeNumber", {}).get("parsed_value", None)


        # TODO: Validate amount/phone number is valid
        # and generate a unique order_id and payment_url
        payment_url = "https://verloop.io/pricing.html"
        self.state["order_id"] = "shfi2387642kahr29"

        self.export(PaymentOptions=[
                        url(title="Pay Rs.{}".format(amount),
                            url=payment_url),
                        postback(title="Payment Done",
                                 action=action(next_block="Verify_Payment"))
                    ])
        return

        #If invalid operator or amount is given return this
        # self.next_block(name="Invalid_Options")
        # self.export(PaymentOptions=[])

    def Check_Payment(self, *args, visitor, variables, state, **kwargs):
        order_id = state.get("order_id")

        # Verify that payment is done for order_id
        # If success
        self.next_block(name="Order_Success")
        self.variable(successInfo="Payment is successful")
        return

        #If failure
        # self.next_block("Order_Failure")
        # self.variable(failureInfo="Payment failed due to whatever reason")

    def _is_valid_op(self, operator):
        valid_ops = ["vodafone", "airtel", "jio", "idea", "aircel"]
        return operator.get("parsed_value") in valid_ops