# print("Python script is running!")
# import pandas as pd

# # Example customer messages
# messages = [
#     "   My strawberries are rotten.   ",
#     "My order     has not arrived.",
#     "  I want a refund.  "
# ]

# df = pd.DataFrame({"body": messages})

# print("Before cleaning:")
# print(df["body"])

# # Remove spaces from beginning and end
# df["body"] = df["body"].str.strip()

# # Replace multiple spaces with a single space
# df["body"] = df["body"].str.replace(
#     r"\s+", " ", regex=True
# )

# print("\nAfter cleaning:")
# print(df["body"])


import pandas as pd

# 1. Load the original dataset
df = pd.read_csv("data/support_tickets.csv")

print("Original dataset shape:", df.shape)

# 2. Select columns containing text
text_columns = [
    "subject",
    "body",
    "correct_reply",
    "category"
]

# 3. Clean unnecessary spaces
for column in text_columns:
    df[column] = (
        df[column]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

# 4. Save the cleaned dataset
df.to_csv(
    "data/cleaned_support_tickets.csv",
    index=False
)

print("Text cleaning completed!")
print("Total tickets:", len(df))
print("Cleaned dataset saved successfully.")
