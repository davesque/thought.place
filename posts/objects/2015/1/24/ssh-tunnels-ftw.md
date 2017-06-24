---
title: SSH Tunnels for Mobile Development
published: 2015-01-24T09:00:00-0400
---

## The Problem:

You are developing a site locally and eventually find yourself needing to test
in a mobile browser.  You try a few things like using Chrome's device emulator
or pushing style updates to a development server in the cloud.  There are
issues with both of these solutions.  Chrome's device emulator doesn't fully
(even remotely) replicate a mobile browser.  Pushing style updates to a dev
server is a pain and may even break your normal staging process.

So what else can you do?  Well...why not just use a mobile phone?  But wait.
How can you use a mobile phone to browse a site being hosted locally on your
development machine?  Your development rig is on your ISP's network behind a
NAT and has no public IP.  As it turns out, this problem has been solved since
before mobile phones were even a thing!

## The Solution:

Enter SSH tunnels.  SSH tunnels provide an easy way to direct data between TCP
ports on systems connected via SSH.  Using an SSH tunnel, you can tell a remote
system (a public web server, for instance) to take any data coming in through
connections on its port 8000, transfer it over an SSH connection to your local
machine, and send it into your local port 80.  As you may now realize,
something like this could allow you to access a site running on your local dev
setup from a mobile phone.

To accomplish this, here's what you'll need:

1. SSH access to a remote system with a static IP
2. Admin rights on the remote system (unless it's already configured for public
   port forwarding)

After doing everything described below, we should be able to make a web request
to a server hosted in the cloud and receive a response from a site running on
our local machine like so:

```
$ curl http://example.com:8000/
<html>
  <body>
    Local content!
  </body>
</html>
```

## The Steps:

**<span style="color: red;">!! Warning !!</span>** The steps in this section
should be undone when mobile testing is finished.  All of them require a
loosening of security restrictions that are in place for good reason.  Do not
leave any of these settings active after you're finished testing!

### Temporarily open firewall

First, ensure that port 8000 is open to incoming and outgoing traffic on the
remote server.  If a firewall is blocking it (which it probably should be!),
then you won't get very far.

### Temporarily enable "GatewayPorts" option for sshd

Next, you'll need to configure `sshd` on the remote system to allow connections
on forwarded ports which are not being made through the loopback interface.  By
default, and for good reason, `sshd` only permits traffic on forwarded ports
from the local system.  This means that, normally, you could only access your
dev site from the remote system in this way:

```
$ curl http://localhost:8000/
<html>
  ...
</html>
```

To change this, you'll need to edit your `sshd` config (probably found at
`/etc/ssh/sshd_config`) and restart `sshd`.  Add or edit `sshd_config` to
include the following line:

```conf
GatewayPorts yes
```

...and restart the SSH daemon: `sudo service ssh restart`

### Ensure your local site is configured to recognize the remote domain

Whether you're typing a domain name into your mobile browser's location bar or
just a straight IP, your local site will need to correctly serve content based
on the HTTP `Host` header.  The easiest way to accomplish this is to tell your
site to serve content for _any_ `Host` header.  With the Django framework for
Python, you would add the following to a _**development**_ settings file:

```python
ALLOWED_HOSTS = ['*']
```

Did I mention that you should only use this kind of setting in
_**development**_?  Well, I'll say it again.  In the case of Django, this
setting is used to prevent attackers from inserting their own host name into
requests and maliciously directing users to their own site.  Make sure you
don't use a setting like this in production.

### Connect to the remote server with tunneling

Now, let's actually make the tunnel.  Login to the remote server with the
following command:

```
$ ssh -R 0.0.0.0:8000:localhost:80 <user>@example.com
```

This should look pretty familiar, but with the addition of the `-R` option.
Let's take a look at the different parts of the argument for this option.  The
`0.0.0.0:8000` part tells ssh to allow any IPv4 address to bind to the
forwarded port 8000 on the remote server.  The `localhost:80` part tells ssh to
take any traffic coming into this forwarded port and direct it to port 80 on
your local machine.

Now that you've got this all set up, open up your mobile browser and navigate
to `http://example.com:8000/`.  You should end up seeing content served by your
local dev site.  Happy mobile stylesheet editing!
