import os
import sys
import argparse
from m2r import convert

def processTocRow(docTitle, section, title, content):
    #print(f'\tSection: {section} Heading Level: {level} Title: {title} Content File: {content}')
    output = ""

    level = len(section.split(".")) + 1

    if (len(title) > 0):
        # Add section heading
        output += ('#' * level) + " " + title + "\n"

    convertToRst = len(content) == 0 or content.endswith(".md")

    # Process content (if present)
    if (len(content) > 0):
        reader = open(content, encoding="utf8")
        try:
            # strip off any Jekyll metadata at the top of the file
            inMetadata = False
            for line in reader.readlines():
                if (line.strip() == "---"):
                    inMetadata = not inMetadata
                    continue
                if (not inMetadata):
                    if (line.startswith("#")):
                        # make sure heading level is correct-ish
                        output += ('#' * level) + line + "\n"
                    else:
                        # append line to output
                        output += line
        finally:
            reader.close()

    rst = ""
    if (convertToRst):
        rst = convert(output)
    else:
        rst = output

    # add a page break    
    rst += "\n.. raw:: pdf\n   \n   PageBreak\n"
    return rst

def processDocFile(docFile):
    category = ""
    title = ""
    order = ""
    level = 0
    output = ""
    reader = open(docFile, encoding="utf8")
    try:
        # strip off any Jekyll metadata at the top of the file
        inMetadata = False
        for line in reader.readlines():
            if (line.strip() == "---"):
                if (inMetadata):
                    output += ('#' * level) + title + "\n"
                inMetadata = not inMetadata
                continue
            if (inMetadata):
                parts = line.split(":")
                if (parts[0].strip() == "category"):
                    category = parts[1].strip()
                    continue
                if (parts[0].strip() == "title"):
                    title = parts[1].strip()
                    continue
                if (parts[0].strip() == "order"):
                    order = parts[1].strip()
                    level = len(order.split("."))
                    #print("order=" + order + "   level=" + str(level))
                    continue
            if (not inMetadata):
                if (line.startswith("#")):
                    # make sure heading level is correct-ish
                    output += ('#' * level) + line + "\n"
                else:
                    # append line to output
                    output += line
    finally:
        reader.close()

    output += "\n"

    return category, order, title, output


def processDocDir(docDir):
    docTitle = ""
    docContent = ""
    for _, _, files in os.walk(docDir):
        files.sort()
        for filename in files:
            docTitle, _, _, content = processDocFile(docDir + "/" + filename)
            docContent += content

    return docTitle, docContent
            

parser = argparse.ArgumentParser()
parser.add_argument("docpath", help="directory containing documents")
parser.add_argument("outpath", help="location to write assembled markdown files")
args = parser.parse_args()

os.makedirs(args.outpath, exist_ok = True)

output = ""

# each directory contains a document, ignore files at this level of the file tree
for root, dirs, _ in os.walk(args.docpath):
    for directoryname in dirs:
        title, content = processDocDir(root + "/" + directoryname)

        # write markdown version of the document
        mdFileName = args.outpath + "/" + title.replace(" ", "_") + ".md"
        f = open(mdFileName, "w")
        f.write(content)
        f.close()

        # write reStructuredText version of the document
        rst = """
.. header:: 

   [[[TITLE]]] 

.. footer::

    |date| ___________________________________________________________________page ###Page###

.. sectnum::
  :depth: 3

[[[DOC_TITLE]]]

.. raw:: pdf

   PageBreak

.. contents:: Table of Contents
   :depth: 3

.. raw:: pdf

   PageBreak

.. |date| date:: %m-%d-%Y
"""
        rst = rst.replace("[[[TITLE]]]", title).replace("[[[DOC_TITLE]]]", ('=' * len(title)) + "\n" + title + "\n" + ('=' * len(title)))
        rst += convert(content)
        rstFileName = args.outpath + "/" + title.replace(" ", "_") + ".rst"
        f = open(rstFileName, "w")
        f.write(rst)
        f.close()
       
        



#print(output.replace("Release X.Y.Z", "Release " + args.rel))
 
