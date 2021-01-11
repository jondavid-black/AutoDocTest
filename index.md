---
title: Welcome
---

This is an experiment to explore the applicaiton of DevOps principles to documentation.  Those of us who work in the defense industry spend countless hours (and likely millions of dollars) just trying to manage and publish documents or document changes.  Almost everything we do revolves around documents in some form - from plans, procecures, and work instructures that describe how we work to engineering documents that describe what we build.  

This experiment attempts to explore a simple strategy:  segregate documents by major section (which usually aligns to author) and publish in a web first manner while still supporting traditional PDF deliverables.  To explore this space I've searched the internet to find examples of government documents that have the look and feel of the sort of documents we often encounter.

### Technology

The technology selected is intended to be universally available to anyone who would like to use it.  Everything is free and open source.

- Markdown 
- Jekyll ( using the **Edition** template from [CloudCannon](http://cloudcannon.com/) )
- Python
- reStructuredText

In this example, configuration management is done through Git and GitHub but should be transferrable to other (similar) environments.  Continuous Integration is done using GitHub Actions, but are little more than scripted execution of common linux commands or python scripts contained within this repository.

### Future

Although I've put some energy into depicting each section of published documents individually, I really don't care for the user experience that results.  I may explore consolidating each document to a single page, or perhaps just providing a "full doc pop out" for those who may prefer a "single pane of glass" to read and scroll around documents.

### DevOps for Defense

This experiment has been done in support of the [DevOps for Defense](https://devopsfordefense.org) meetup.  Please join us on the first Thursday of each month, check out our YouTube channel, or offer to contribute a talk to our community.  Thanks!