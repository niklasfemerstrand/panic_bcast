# panic_bcast #

panic_bcast is a network protocol panic button operating decentralized through UDP broadcasts and HTTP. It’s intended to act a panic button in a sensitive network making it harder to perform cold boot attacks. A serious freedom fighter will run something like this on all nodes in the computerized network.

## How it works ##

1. An activist has uninvited guests at the door
2. The activist sends the panic signal, a UDP broadcast, with panic_bcast
3. Other machines in the network pick up the panic signal
4. Once panic_bcast has picked the panic signal it kills truecrypt and powers off the machine.

panic_bcast was written with the intention to support any form of UNIX that can run Python. It has been successfully tested on FreeBSD and Linux.

To trigger the panic signal over HTTP simply request http://...:8080/panic from a machine that is running panic_bcast. Which ever will do.

Please note that panic_bcast is a beta and more sophisticated ways to prevent cold boot attacks are planned. You can view these plans by searching for the word "TODO" in the source code.

Remember kids: there's no home for swap in opsec.
