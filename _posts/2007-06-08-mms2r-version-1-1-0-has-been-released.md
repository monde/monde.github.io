---
title: "mms2r version 1.1.0 has been released!"
date: 2007-06-08
categories: [Ruby, MMS2R]
tags: [mms2r, ruby]
---

mms2r version 1.1.0 has been released!

- http://mms2r.rubyforge.org/

1. DESCRIPTION:

MMS2R is a library that decodes the parts of an MMS message to disk while
stripping out advertising injected by the cellphone carriers. MMS messages are
multipart email and the carriers often inject branding into these messages. Use
MMS2R if you want to get at the real user generated content from a MMS without
having to deal with the cruft from the carriers.

If MMS2R is not aware of a particular carrier no extra processing is done
to the MMS other than decoding and consolidating its media.

Contact the author to add additional carriers to be processed by the
library. Suggestions and patches appreciated and welcomed!

Corpus of carriers currently processed by MMS2R:

- AT&T/Cingular => mmode.com
- Cingular => mms.mycingular.com
- Cingular => cingularme.com
- Dobson/Cellular One => mms.dobson.net
- Nextel => messaging.nextel.com
- Sprint => pm.sprint.com
- Sprint => messaging.sprintpcs.com
- T-Mobile => tmomail.net
- Verizon => vzwpix.com
- Verizon => vtext.com

Changes:

1. 1.1.0 / 2007-06-08 (Toki Wartooth)

- get\_body to return body text (Luke Francl)
- get\_subject returns ”” for default subjects now
- default subjects listed in yaml by carrier in conf directory
- added granularity to Cingular, Sprint, and Verizon carrier services (Will Jessup)
- refactored Sprint instance to process all media (Will Jessup + Mike)
- optimized text transformations (Will Jessup)
- properly handle ISO-8859-1 and UTF-8 text (Will Jessup)
- autotest powers activate! (ZenTest autotest discovery enabled)
- configuration file ignores, transforms, and subjects all store Regexp’s
- Put vendor Text::Format & TMail::Mail as an external subversion dependency
  to the 1.2 stable branch of Rails ActionMailer
- added get\_number method to return the phone number associated with this MMS
- get\_media and get\_text attachment\_fu helper return the largest piece of media
  of that type if the more than one exits in the media (Luke Francl)
- added block support to process() method (Shane Vitarana)

- http://mms2r.rubyforge.org/
