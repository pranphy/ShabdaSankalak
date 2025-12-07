import re
from datasets import load_dataset

# Load JSON file into a Hugging Face Dataset
#cdataset = load_dataset("json", data_files="articles_clean.json")
#tdataset = load_dataset("json", data_files="transliterated_dataset.json")

cdataset = load_dataset("json", data_files="data/**/*.json")
dataset = cdataset

print(dataset)

#  urls = cdataset["train"]["url"]

#  #Regex to capture /YYYY/MM/DD/
#  pattern = re.compile(r"/(\d{4}/\d{2}/\d{2})/")
#  
#  dates = set()
#  for url in urls:
#      match = pattern.search(url)
#      if match:
#          dates.add(match.group(1))
#  
#  # Print all unique dates
#  for d in sorted(dates):
#      print(d)

