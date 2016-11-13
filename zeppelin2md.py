#!/usr/bin/python

import json
import codecs
import sys

def getMode(paragraph):
  mode = None
  text = paragraph.get("text")
  line1 = text.split("\n")[0]
  if len(line1) > 0 and line1[0] == "%":
    mode = line1[1:]
  else:
    if paragraph["config"].get("editorMode"):
      mode = paragraph["config"].get("editorMode").split("/")[-1]
  
  if mode is None or mode == "md":
    mode = "markdown"

  return mode

def fprint(line=""):
  fout.write(line.encode("utf-8") + "\n")

def writePreamble(jsonFile, githubRepository):
  fprint(">**Note:**")
  fprint(">This Readme has been automatically created by [zepppelin2md.py](https://github.com/bernhard-42/zeppelin2md).\n")
  fprint(">Alternatively, to open the Zeppelin Notebook with [Zeppelin Viewer](https://www.zeppelinhub.com/viewer) use the URL ")
  fprint(">    `https://raw.githubusercontent.com/bernhard-42/%s/master/%s`" % (githubRepository, jsonFile))
  fprint("\n# %s" % jsonFile)

jsonFile = sys.argv[1]
githubRepository = sys.argv[2]

note = json.load(codecs.open(jsonFile, 'r', 'utf-8-sig'))

with open("Readme.md", "w") as fout:
  writePreamble(jsonFile, githubRepository)

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

