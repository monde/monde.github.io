---
title: "handling a rcov non-dependency in your gem on firebrigade"
date: 2007-06-11
categories: [Ruby, Seattle.rb, Gems, MMS2R]
tags: [firebrigade, gems, mms2r, ruby]
---

MMS2R was not showing any tests in its [firebridge entry](./gem/show/mms2r/index.html) because I had a non-dependency for a rcov task that I had included in the MMS2R gem’s Rakefile

This is what Eric says on firebrigade:

[Depend on what you need so that your tests will work. For example, if you have an rcov task, but you don’t want to mark it as a dependency, wrap it in a rescue block. Tinderbox is friendly enough to add Rake or RSpec as a dependency if you forgot it, but other than that, you’re on your own.](./home/gem_developers/index.html)

This is how to rescue the LoadError exception around the require statement for rcov in the [Rakefile](./cgi/viewvc.cgi/trunk/index.html) :

```
begin
  require 'rcov/rcovtask'
rescue LoadError
end
```

and this is how I rescue the NameError exception in the rcov task:

```
begin
  Rcov::RcovTask.new do |t|
    t.test_files = FileList['test/test*.rb']
    t.verbose = true
    t.rcov_opts << "--exclude rcov.rb,hpricot.rb,hpricot/.*\.rb" 
  end
rescue NameError
end
```

**update**

*07/04/2007*

Actually MMS2R is not being tested on the firebrigade currently. The problem stems from a bug in Gems 0.9.4 where MMS2R being dependent on Hpricot and Tinderbox getting a Gem::RemoteInstallationCancelled exception (line 106 of lib/tinderbox/gem\_runner.rb) that Eric transforms into a Tinderbox::ManualInstallError

```
/usr/local/lib/ruby/gems/1.8/gems/tinderbox-1.0.0/lib/tinderbox/gem_runner.rb:108:in `install': Installation of mms2r-1.1.2 requires manual intervention (Tinderbox::ManualInstallError)
        from /usr/local/lib/ruby/gems/1.8/gems/tinderbox-1.0.0/lib/tinderbox/gem_runner.rb:265:in `run'
        from /usr/local/lib/ruby/gems/1.8/gems/tinderbox-1.0.0/bin/tinderbox_gem_build:9
        from /usr/local/bin/tinderbox_gem_build:16:in `load'
        from /usr/local/bin/tinderbox_gem_build:16
```

Eric says its an known bug in Gems 0.9.4 and should bug them about it!
