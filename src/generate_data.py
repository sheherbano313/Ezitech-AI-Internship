
import pandas as pd
from pathlib import Path

# Dataset output location
output_path = Path("data/support_tickets.csv")

# 20 realistic FreshCart customer support tickets
tickets = [
    {
        "id": "FC001",
        "subject": "Damaged organic apples",
        "body": "I received my organic apples today, but several of them are bruised and damaged. What can I do?",
        "correct_reply": "We apologize for the condition of your apples. Please share a photo of the damaged items and your order number with our support team. We will review your request and assist with an eligible refund or replacement.",
        "category": "Organic Produce Quality"
    },
    {
        "id": "FC002",
        "subject": "Wilted spinach received",
        "body": "The spinach in my grocery order looks wilted and is not fresh. I expected better quality.",
        "correct_reply": "We are sorry that the spinach did not meet your expectations. Please provide your order number and a photo of the product so our team can review the quality issue and guide you through the available resolution.",
        "category": "Organic Produce Quality"
    },
    {
        "id": "FC003",
        "subject": "Mold on strawberries",
        "body": "I opened my strawberry package and noticed mold on some of the strawberries.",
        "correct_reply": "We apologize for this experience. Please do not consume the affected strawberries. Share a photo and your order number with our support team so we can review the issue and arrange an appropriate resolution.",
        "category": "Organic Produce Quality"
    },
    {
        "id": "FC004",
        "subject": "Incorrect organic vegetables",
        "body": "I ordered organic carrots but received regular carrots instead. Can you help?",
        "correct_reply": "We are sorry for the incorrect item. Please share your order number and a photo of the received product. Our support team will verify the issue and help with a suitable resolution.",
        "category": "Organic Produce Quality"
    },
    {
        "id": "FC005",
        "subject": "Delivery is late",
        "body": "My grocery delivery was scheduled for 2 PM, but it has not arrived yet. Can you check?",
        "correct_reply": "We apologize for the delay. Please share your order number so our support team can check the delivery status and provide an updated estimated arrival time.",
        "category": "Delivery Delays"
    },
    {
        "id": "FC006",
        "subject": "Order not delivered",
        "body": "My order status says delivered, but I have not received anything.",
        "correct_reply": "We are sorry for the confusion. Please confirm your order number and delivery address. Our team will investigate the delivery status and contact the delivery partner if necessary.",
        "category": "Delivery Delays"
    },
    {
        "id": "FC007",
        "subject": "Delivery driver is late",
        "body": "The delivery driver called me but still has not reached my location.",
        "correct_reply": "We apologize for the inconvenience. Please share your order number so we can check with the delivery team and help you get an updated delivery estimate.",
        "category": "Delivery Delays"
    },
    {
        "id": "FC008",
        "subject": "Change delivery time",
        "body": "I will not be home during the scheduled delivery time. Can I reschedule my order?",
        "correct_reply": "We can check whether your delivery can be rescheduled. Please provide your order number and preferred delivery time. Changes depend on the order status and available delivery slots.",
        "category": "Delivery Delays"
    },
    {
        "id": "FC009",
        "subject": "Refund for missing item",
        "body": "I paid for milk, but it was missing from my delivered order. I want a refund.",
        "correct_reply": "We apologize for the missing item. Please share your order number and confirm which item was missing. Our team will verify the order and review your refund request.",
        "category": "Refunds and Returns"
    },
    {
        "id": "FC010",
        "subject": "Refund status",
        "body": "My refund was approved several days ago, but I still cannot see the amount in my account.",
        "correct_reply": "We understand your concern. Please share your order number and refund confirmation details. Our support team will check the refund status and provide an update. Processing time may depend on your payment provider.",
        "category": "Refunds and Returns"
    },
    {
        "id": "FC011",
        "subject": "Request refund for poor quality",
        "body": "The vegetables I received were poor quality. Can I request a refund?",
        "correct_reply": "We are sorry about the product quality. Please send your order number and clear photos of the affected vegetables. Our team will review the request according to the applicable quality and refund policy.",
        "category": "Refunds and Returns"
    },
    {
        "id": "FC012",
        "subject": "Return an unwanted item",
        "body": "I ordered the wrong product by mistake. Can I return it?",
        "correct_reply": "Please share your order number and the product details. Our team will check whether the item qualifies for return under the applicable FreshCart return policy.",
        "category": "Refunds and Returns"
    },
    {
        "id": "FC013",
        "subject": "Missing grocery items",
        "body": "My delivery arrived, but two items from my order are missing.",
        "correct_reply": "We apologize for the incomplete order. Please provide your order number and list the missing items. Our team will verify the order and assist with an appropriate resolution.",
        "category": "Missing or Damaged Items"
    },
    {
        "id": "FC014",
        "subject": "Broken egg carton",
        "body": "Several eggs were broken when my grocery order arrived.",
        "correct_reply": "We are sorry that your eggs arrived damaged. Please share a photo of the broken eggs and your order number so our team can review the issue and help resolve it.",
        "category": "Missing or Damaged Items"
    },
    {
        "id": "FC015",
        "subject": "Wrong product delivered",
        "body": "I ordered orange juice but received apple juice instead.",
        "correct_reply": "We apologize for the incorrect delivery. Please share your order number and a photo of the received product. Our support team will verify the mistake and assist with the next steps.",
        "category": "Missing or Damaged Items"
    },
    {
        "id": "FC016",
        "subject": "Cancel grocery order",
        "body": "I placed an order by mistake and want to cancel it immediately.",
        "correct_reply": "We can check whether cancellation is still possible. Please provide your order number. Cancellation depends on the current order preparation and dispatch status.",
        "category": "Order Cancellation"
    },
    {
        "id": "FC017",
        "subject": "Cancel an order after dispatch",
        "body": "My order has already been dispatched, but I no longer need it. Can I cancel?",
        "correct_reply": "We understand your request. Since the order has been dispatched, cancellation may no longer be available. Please share your order number so our team can check the available options.",
        "category": "Order Cancellation"
    },
    {
        "id": "FC018",
        "subject": "Payment deducted twice",
        "body": "My bank account shows two deductions for one FreshCart order.",
        "correct_reply": "We apologize for the concern. Please share your order number and the transaction references, without sharing your full card number or PIN. Our team will investigate the duplicate charge.",
        "category": "Payment Issues"
    },
    {
        "id": "FC019",
        "subject": "Payment failed but money deducted",
        "body": "The checkout page showed payment failed, but money was deducted from my bank account.",
        "correct_reply": "We understand your concern. Please share your order number and transaction reference. Our team will investigate the payment status. Do not share your PIN, password, or full card details.",
        "category": "Payment Issues"
    },
    {
        "id": "FC020",
        "subject": "Store operating hours",
        "body": "What are FreshCart's opening and closing hours?",
        "correct_reply": "Thank you for contacting FreshCart. Our operating hours are not specified in this sample knowledge base. Please contact the store directly to confirm its current opening and closing times.",
        "category": "General Store Policies"
    }
]

# Convert records into a DataFrame
df = pd.DataFrame(tickets)

# Save as CSV
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False, encoding="utf-8")

print("Dataset created successfully!")
print("Total tickets:", len(df))
print("Columns:", list(df.columns))
print("Saved to:", output_path)
