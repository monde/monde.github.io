---
title: "mms2r 1.0.7 Released!"
date: 2007-04-27
categories: [Ruby, Seattle.rb, Nuby Rails, Gems]
tags: [gems, ruby]
---

mms2r version 1.0.7 has been released!

```
http://mms2r.rubyforge.org/
```

```
DESCRIPTION:
```

MMS2R is a library that decodes the parts of an MMS message to disk while
stripping out advertising injected by the cellphone carriers. MMS messages are
multipart email and the carriers often inject branding into these messages. Use
MMS2R if you want to get at the real user generated content from a MMS without
having to deal with the garbage from the carriers.

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

1.0.7 / 2007-04-27 (Senator Stampingston)

- patch submitted by Luke Francl
- added a get\_subject method that returns nil when any MMS has a default carrier subject
- get\_subject returns nil for ’’, ‘Multimedia message’, ‘(no subject)’, ‘You have new Picture Mail!’

  http://mms2r.rubyforge.org/
