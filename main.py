import CobolParser
import CobolSummarizer

def main():
  # 1. Parse
  parser = CobolParser(cobol_code)
  parsed = parser.parse()
  
  # 2. Summarize
  summarizer = CobolSummarizer(client, "gpt-4o")
  
  paragraph_docs = {}
  
  for para_name, para_code in parsed["paragraphs"].items():
      paragraph_docs[para_name] = summarizer.summarize_paragraph(
          para_name,
          para_code
      )

if __name__() == "main":
  main()
