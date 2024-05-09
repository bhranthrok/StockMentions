# Script to extract company names from the NASDAQ .csv so we can use them as a stock mention

import pandas as pd

# Load a custom Excel file made from the first 2 columns of the NASDAQ and NYSE .csv's
filePath = r"F:\Projects\StockMentions\StockMentions\NASDAQ Name Extraction\StockVariationsList.xlsx"
df = pd.read_excel(filePath)

# Looks for a keyword and extracts everything before it
def extractName(fullName):
    keywords = [".com", " technology", " technologies", " pharma", " therap", " acquisition", " entreprise",
                 " investment", " global", " limited", " inc", " corp", " co.", " company", " group", " s.a.",
                   " lp", " l.p.", " ltd", " plc", " llc", " depositary", " ordinary", " common", " shares"]
    for keyword in keywords:
        if keyword in fullName.lower():
            extractedName = fullName.lower().split(keyword)[0].strip()
            return extractedName
    return fullName

# Apply extraction
df["Extracted Name"] = df["Name"].apply(extractName)

# Save to new file
outputFilePath = r"F:\Projects\StockMentions\StockMentions\NASDAQ Name Extraction\ExtractedStockVariationsList.xlsx"
df.to_excel(outputFilePath, index=False)

print("Extraction completed. Output saved to:", outputFilePath)
