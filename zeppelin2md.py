#!/usr/bin/python

import json
import codecs
import sys

def getMode(paragraph):
  mode = None
  if paragraph["config"].get("editorMode"):
    mode = paragraph["config"].get("editorMode").split("/")[-1]
  else:
    text = paragraph.get("text")
    line1 = text.split("\n")[0]
    if len(line1) > 0 and line1[0] == "%":
      mode = line1[1:]
  
  if mode == "md":
    mode = "markdown"

  return mode

def fprint(line=""):
  fout.write(line.encode("utf-8") + "\n")


note = json.load(codecs.open(sys.argv[1], 'r', 'utf-8-sig'))

with open("Readme.md", "w") as fout:
  for paragraph in note["paragraphs"]:
    if "text" in paragraph.keys():
      text = paragraph["text"].split("\n")

      while (len(text[0]) == 0):    # remove empty lines at the beginning ...
        text = text[1:]
      while (len(text[-1]) == 0):   # ... and at the end
        text = text[:-1]

      mode = getMode(paragraph)

      if mode == "markdown":
        text = text[1:]
      elif mode == "scala":
        text = ["%spark"] + text
      elif mode == "python":
        text = ["%pyspark"] + text

      fprint("\n---\n")

      if paragraph["config"].get("title"):
        fprint("#### %s" % paragraph["title"])

      if mode == "markdown":
        for line in text:
          fprint(line)
      else:
        fprint("\n_Input:_\n")
        indent = ""
        if mode == "scala":
          fprint("```scala")
        elif mode == "python":
          fprint("```python")
        elif mode == "sh":
          fprint("```bash")
        elif mode == "dep":
          fprint("```scala")
        elif mode == "sql":
          fprint("```sql")
        for line in text:
          fprint(indent + line)
        fprint("```")
      fprint()

    if "result" in paragraph.keys():
      if paragraph["result"]["type"] == "TEXT" and mode != "markdown":
        if len(paragraph["result"]["msg"]) > 0:
          fprint("\n_Result:_\n")
          result = paragraph["result"]["msg"].split("\n")
          fprint("```")
          for line in result:
            fprint(line)
          fprint("```")

