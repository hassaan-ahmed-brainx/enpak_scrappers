import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

spiders = subprocess.run(["scrapy", "list"], stdout=subprocess.PIPE, text=True).stdout.strip().split('\n')

def run_spider(spider_name):
  log_file = f"logs/{spider_name}_logs.txt"
  os.makedirs(os.path.dirname(log_file), exist_ok=True)

  with open(log_file, 'w') as file:
    file.truncate()
    subprocess.run(
      ["scrapy", "crawl", spider_name],
      check=True,
      stdout=file,
      stderr=subprocess.STDOUT
    )
  print(f"{spider_name} completed and logged to {log_file}")

for spider in spiders:
    run_spider(spider)
