---
title: "Processing Cellphone MMS Messages With Ruby"
date: 2007-02-11
categories: [web2.0, Ruby, Seattle.rb, Nuby Rails]
tags: [mail, mms, ruby]
---

Cellphone Multimedia Message Service (MMS) messages that your cellphone sends are really just email formatted text. You can send MMS to other cellphones or to a real email address. I wrote a post about using the Rails receive method in ActionMailer::Base to process email [decoding email attachments with ActionMailer::Base receive](./articles/2006/12/30/decoding-email-attachments-with-actionmailer-base-receive) If you just want to process the mail but don’t need the hook into Rails then just use the TMail class’s parse method directly

```
mail
 
=
 
TMail
::
Mail
.
parse
(
raw_email
)
```

I’ve been processing MMS emails via TMail recently and have found the cellphone carriers often modify user generated content (text, videos, images) to include advertising for their services.

I was talking to Geoffrey Grosenbach of [Nuby On Rails](./index.html) at a Seattle.rb meeting and told him about my travels with MMS. He said that he’s working on something that could use this experience and suggested that I write a gem for it. I think I will write a gem so really this post is to see if I can get any feed back from the community.

I think I will call the gem mms2r because I want to transform an MMS message into a Ruby class. I want my MMS2R class to do three things very well:

- Extract the real text from the sender stripping out any advertising that the cellphone carriers annoyingly add to their messages. Also strip out any HTML formatting.
- Extract the real image(s) that can be packaged into an MMS
- Extract the real video(s) that can be packaged into an MMS

I live in the Pacific Northwest and the cellphone carriers that I know about here are old AT&T accounts now under Cingular, Cingular, Sprint, T-Mobile, and Verizon.

AT&T (MMode), Cingular, T-Mobile, and Verizon, all send real MMS messages. What I mean by that is if you send a picture via MMS then that picture file is contained as a multipart part in the message. The same holds true of video files.

The one deviant is Sprint. They send a multipart message and the plain text part is a link back to their media hosting servers and the text/html part are links to the advertising and the media hosting server. So in order for you to see your friend’s Sprint cellphone images and videos you have to go to Sprint’s web site to view that content.

The other carriers are not completely saints either. Cingular is best, its multipart mails contain no advertising wrapped around the real data from the user. However, just a plain text Cingular message (via SMS) has a advertising footer added to the message. Images and video from T-Mobile include additional images as multiparts that are used in a text html wrapper of the content. The wrapper has advertising for T-Mobile. You can discard all the multiparts from T-Mobile and just focus on the real image or video without any extra processing. Verizon as injects an adverting footer onto the plain text message created by the user.

So I just signed up for a rubyforge account and submitted a project request. We’ll see what happens.

I was talking to Geoffrey Grosenbach of [Nuby On Rails](./index.html) at a Seattle.rb meeting and told him about my travels with MMS. He said that he’s working on something that could use this experience and suggested that I write a gem for it. I think I will write a gem so really this post is to see if I can get any feed back from the community.

I think I will call the gem mms2r because I want to transform an MMS message into a Ruby class. I want my MMS2R class to do three things very well:

- Extract the real text from the sender stripping out any advertising that the cellphone carriers annoyingly add to their messages. Also strip out any HTML formatting.
- Extract the real image(s) that can be packaged into an MMS
- Extract the real video(s) that can be packaged into an MMS

I live in the Pacific Northwest and the cellphone carriers that I know about here are old AT&T accounts now under Cingular, Cingular, Sprint, T-Mobile, and Verizon.

AT&T (MMode), Cingular, T-Mobile, and Verizon, all send real MMS messages. What I mean by that is if you send a picture via MMS then that picture file is contained as a multipart part in the message. The same holds true of video files.

The one deviant is Sprint. They send a multipart message and the plain text part is a link back to their media hosting servers and the text/html part are links to the advertising and the media hosting server. So in order for you to see your friend’s Sprint cellphone images and videos you have to go to Sprint’s web site to view that content.

The other carriers are not completely saints either. Cingular is best, its multipart mails contain no advertising wrapped around the real data from the user. However, just a plain text Cingular message (via SMS) has a advertising footer added to the message. Images and video from T-Mobile include additional images as multiparts that are used in a text html wrapper of the content. The wrapper has advertising for T-Mobile. You can discard all the multiparts from T-Mobile and just focus on the real image or video without any extra processing. Verizon as injects an adverting footer onto the plain text message created by the user.

So I just signed up for a rubyforge account and submitted a project request. We’ll see what happens.
