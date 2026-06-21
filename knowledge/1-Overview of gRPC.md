https://www.youtube.com/watch?v=sImWl7JyK_Q


# [Title of Presentation / Article / Paper]

**Author/Speaker:** [Name]

**Date:** [YYYY-MM-DD]

**Source/Event:** [Link, Journal Name, Conference, etc.]

**Tags:** #tag1 #tag2 #tag3

**Written by:**

**Read by:**

---

## 💡 The TL;DR (Executive Summary)
Lorem Ipsum
## 🎯 Key Arguments & Main Points
* **Point 1:** 
    * *Evidence/Detail:*
* **Point 2:**
    * *Evidence/Detail:*
* **Point 3:**
    * *Evidence/Detail:*

## 📝 Important Details & Quotes
* "[Insert powerful quote here]" - (Page/Timestamp)


## 🧠 Synthesis & Personal Reflections
*This is the most important section. Do not just record; react.*
* **Why does this matter?**
* **How does this connect to my current knowledge or projects?**
* **Do I agree or disagree? Why?** 

## ❓ Questions & Gaps
*What wasn't explained well? What are you curious about now?*

## ✅ Action Items & Follow-Up
*What do you need to do because of this information?*
* [ ] Look up: [Concept or terminology you didn't understand]
* [ ] Read related paper: [Title/Author mentioned]
* [ ] Apply [Specific idea] to [Your project]




## Transcript of [gRPConf 2024 Keynote] Overview of gRPC | Ivy Zhuang, Google
Check out the codelabs to get hands-on experience with gRPC:

https://codelabs.developers.google.com/grpc

### What is gRPC?
A cutting-edge open source high-performance state-of-the-art Remote Procedue Call (RPC) framework developed by Google.

Go-to standard in industry. 

### gRPC Use Cases:

gRPC use cases everywhere it enables communication between a wide
range of devices from the mobile phone
to web browser to desktops and to
various backend platforms this versatility makes it
perfect to building microservices and
distributed applications whether in on
premise in the cloud or in the
containers

### Why gRPC is outstanding

gRPC is popular because it is
* suitable for many needs in addition to
being available in a wider range of
platforms and language the performance
is industry leading 
* it is blazing fast incredibly efficient that connects your application and services at very reliable and a smooth way
* Many components in gRPC are designed
to be plugable like there are different
transport suitable for different devices
and environments like you can specify
civilization wire format or you can
specify interceptors Etc this all makes
integrating with your development stack
very efficient and
flexible gRPC has Rich features around
the um core traffic management or
security and the tailored ones for PIV
uh for service match just to name a few
let's expand more on all of these
Dimensions gp's popular popularity
stands on a few key fundamental design
decisions that brings in Cutting Edge
Technologies on top of it one is that
gRPC is using protuff for data calization
and generating
interfaces protuff is an open source
language agnos framework uh all of the
grpc Implement uh language
implementations use protuff plugin to
generate interfaces therefore these
language uh these gRPC language can talk
with each other over various devices and
platforms Pabu uses binary encoding it
is very efficient in parsing and reduces
message sizes all of which make gRPC high
performance and high flexibility
compared with other RPC
Frameworks gRPC boasts an extensive
support of languages and platforms as
evidenced from this
list um the exciting news as Kevin abek
mentioned that Russ JP R is coming soon
so uh don't miss out today's session if
you want to learn more about
it another key design decision is that
your PC is built on top of http2 that
make it compatible with with a variety
of low balancers and practice over the
wild
internet hp2 reduces TCP connection is
binary and use header compression all of
which makes grpc high performance reduce
latency and make better use of
resources okay Core Concepts so gpc's
core concept starts with channel channel
is an abstract of the end point that you
can send or receive messages
it is the first object that you will
create when you are using JPC to create
a channel you will provide the talk UI
string to specify the remote Hoster name
and then Channel credentials for
authorization again I highly recommend
to attend those collabs to gain more
practical experiences
quickly so as a channel is like a
waterpipe placeholder the sub channels
are the real connections towards the
back end um Services JPC during it life
cycle will create those sub channels
dynamically select sub channels to
multipli rpcs over the channel and it
will report Channel status and finally
tear down the sub channels to return
resources JPC is very simple to use the
application only need to send a request
of the stop that is Created from the
channel and stop is at the protuff
generated layer which is also the first
layer that you will see when you're
using
gRPC the stop qu call towards the gRPC run
time and then further creates stream on
the transport so in gRPC an RPC a core or
stream are fundamentally the same
concept just refer to by different names
at various um stages in their life
cycle because the chance part speakers
IP address while you specify or Target
UI screen when you are creating the
channel so the first thing gRPC will do
is to do this uh translation before it
contacts the
internet name resolution is often
thought to be the same as DNS but in
practice however uh name resolution is
often augmented with extensions or
completely replaced to do name
resolution fundamentally name resolution
is a service Discovery and it's
pluggable you can bring in the custom
name solver by specifying a schema and
then you will put the schema as a syntax
in the Target your string grpc will do
this mapping for
you name resolver returns service config
to the next component which is low
balancer low balancer manages sub
channels create connections and
distribute request among the backend
multiple backhand
Services by taking this service config
low balancer can understand where and
how to route the traffic like which kind
of load Bal type to use their
configurations whether to do health
check
Etc low balancer is a plugable component
the built-in low balancer types are
picked first which is the default and
the r robbing wait R robbing list
request
Etc so for the first time the system
establishes low balancer will um create
connection towards the backend service
um that is listening on the certain
ports when the system is running low
balancer will monitor the connections on
those sub channels and if necessary it
will tear down some sub channels and
replace with new
ones like for example the back end
becomes
unhealthy uh L balancer essentially
divides GP system into control plane and
data plane it maintains a cach cach the
Picker that dynamically selects a sub
channel on the per RPC based routing and
this is on the data plane path while on
the control plane path the low balancer
will swap the cash in flight this
essentially ensures that grpc is
scalable effectively and high
performance lb is one of the most
critical component in GPC so if you're
interested in learning more you can
check out eswa session
today upon the connection establishment
GPC will send a request over the Y
it is using the protuff calization and
the data is framed using htb2
protocol the server side is a mirror of
the client s the server Transportation
once receed the request um will pass up
the messages to the JFC run time toward
the Stop and notifies the
application the application sends a
response back on the
stop gRPC communic back to the client and
depending on how many those kind of
round trips in each RPC GP supports four
types of them unit call is that you only
have one request and response um within
single RPC while by streaming is that
you have multiple on both directions and
similarly for count streaming and server
streaming in principle J is always
asynchronous um but some of apis are
blocking these are just special cases of
the asynchronous
cost you can choose one for your
business bus
logic a few more bonus um tips for the
core comp Concepts in the J life
cycle so at the channel and server layer
interceptors are useful tools to add a
task tasks that are independent of the
methods but apply to all or most of the
rpcs interceptors are very powerful
midle Weare tools to add a tasks to um
modify or replace your your your cost um
before and after they reach their
destination at both the client and the
server
side this provides a very clean way to
um address uh Cutting Edge concerns like
logging authenication authorization like
ever handling monitoring Etc without
cluttering your main application
logic you can provide multiple um client
server interceptors and their order
matters for them example if you are
installing two client interceptors the
caching and loging Interceptor and if
you put log uh caching Interceptor front
then that means you are focusing more on
the communication because the loging
part will be just skipped if you have a
cash hit but if you flipped other to put
the login first then you are observing
more on the client Behavior because all
the requests will be
logged you might find that many of your
functionality is already available as an
Interceptor in in The Wider GPC
ecosystem deadline and time out they are
um when the client is unwilling to wait
for response from a server the client
will receive a deadline exceeded status
code from
gRPC this safeguards against RPC from
taking infinite amount of time when it
is doing um the request especially um in
distributed systems where Network
latency or the servers can cost
L that line can be set from the client
side when it starts an RPC like in this
step um some languages have the concept
of deadline others use idea of time out
well deadline is that is a specific time
point where your RPC cannot go pass by
but the uh time out is the max duration
of the time to compete a RPC these two
concepts are interchangeable with each
other while deadline ex seeded is very
common when the request never leaves the
client for example uh in a typical
scenario that the TCP connection cannot
be established from the lb but when it
leaves the client it will carry this um
deadline information to the server it is
possible that when server first receive
the request it already has earn
realistically small amount of time to
finish at this time it will just cancel
the call and propagate that line
exceeded the status code to the client
while in a distributed application uh it
is typical it's very possible that the
server is also a client towards the
downstream service in this scenario the
um propagating deadline from in incoming
RPC to an ongoing outgoing one is uh is
supported by
gRPC there many benefits of set setting
that line for example you optimize your
resource usage improve latency and abort
long um running operations that are
unlikely to
succeed and it is the best practice to
always set a
deadline while deadline check is
cancellation and user can also actively
termin own outgoing on PC RPC actively
and this is done by do cancel on the
client call object and sometimes on the
context in some
languages like in this code snipp it it
cancel on the future
step the cancellation signal is uh
propagated to the server and normally um
GPC does not have mechanism to interrupt
the server application of this
cancellation but that is not problem the
server can check the cancellation status
on the call and actually to optimize
resource utilization if RPC is long
lived the server Handler should
periodically um check the status of the
call to see whether it is canceled and
cease operation if it does and propagate
the operation downstreams
um by reattempting the failed operations
applications can overcome various
problems temporary issues like Network
or server
glitches your TR component stands in the
core above transport layer and when a TR
happens it will duplicate a stream on
the
transport users uh does not immediately
notice your exists except for increased
latency but with growing the growing
support for observability you can see
more information on retry which is
awesome and let's dive more into the
retry
Logics so grps built in ret logic will
save the call history and then if needed
it will replay the call on uh when
potential retry happens to opt in the
user will specify retry policy in the
service configure so ret policy um
includes say the maximum attempts the
back of policy and retriable status code
list JPC will monitor an um rpc's event
status and if certain criterias are met
for example the retry is with the RPC is
within the maximum attempt and it's
within the retriable status code it will
duplicate a retriable stream on the
transport upon the back off exponential
exponential back of
delays once the response header has been
received
the RPC will hand over to the
application and there will no be no more
tries even without explicit
configuration retry can also happen as a
transparent try it can be multiple
unlimited time of transparent try if the
request never leaves the client or a
single one if it leaves the client but
never seen by the server
application if we config observability
um say open Telemetry then you can see
the ret information for example ret
attempts and the ret latencies on as
open Telemetry Matrix and
chasing when the server receives the
response successfully it can complete
successfully um but there it also
possible that it will um be ended up in
error this is um due to like silver
errors clent cancellation as we talked
or the network errors normally Cent
server will agree on the status of RPC
but it's also possible that for example
the server uh will see the client the
request being successful while due to
communication reasons the client will
see the error status in the client but
this is fine it is important to shut
down server and channel to recollect
resources you will call shutdown on the
channel object that will cancel the new
cost immediately but will let um the
pre-existing cost to continue or you can
also do a forceful shutdown that will
cancel the new and both new and the
pre-existing calls
immediately shutdown is asynchronous you
can call um await domination to wait for
all the resource to be connected and
then it will give up if certain time out
is
reached to summarize today we talked
about grpc Library structure components
we touch a bit on the name resolver and
load balancer and we walked through the
RPC left cycle we talked that uh
application will send messages on the
Stop and the pro on the pro gener layer
and then asynchronously name resolution
will do um uh will do it work and then
the low balancer will establish
connection and pick sub channel for the
request well the initially the RPC will
buffer for a while but the next one it
will be much
faster RPC turned into R tribal stream
at the transport and it might um be
cancelled at any time if that line
exceeded or if there is an explicit
cancellation and finally hopefully the
RPC and all the channel and servers will
be terminated
properly 

gRPC use cases are everywhere. It is especially powerful for building microservices thanks to xDS support in proxies and service meshes solutuions.

Questions:
what is xDS? 
xDS is a set of APIs that allow gRPC to dynamically discover and configure its network behavior, such as load balancing, retries, and circuit breaking. This makes gRPC an ideal choice for building microservices that need to communicate with each other in a dynamic and scalable way.