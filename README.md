# panic_bcast #

panic_bcast is a network protocol panic button operating decentralized through UDP broadcasts and HTTP. It’s intended to act a panic button in a sensitive network making it harder to perform cold boot attacks. A serious freedom fighter will run something like this on all nodes in the computerized network.

panic_bcast was written with the intention to support any form of UNIX that can run Python. It has been successfully tested on FreeBSD and Linux.

To trigger the panic signal over HTTP simply request http://...:8080/panic from a machine that is running panic_bcast. Which ever will do.

## How it works ##

1. An activist has uninvited guests at the door
2. The activist sends the panic signal, a UDP broadcast, with panic_bcast
3. Other machines in the network pick up the panic signal
4. Once panic_bcast has picked the panic signal it kills truecrypt and powers off the machine.

## Authentication ##

If you want you can append the panic signal with a required key. Just execute the script with the -k option. When using the key it is appended to the string "panic"; if your key happens to be "_banana" then the panic signal will respectively be "panic_banana". The panic signal is then sent over the network as a MD5 checksum. Consequently you have to start the script with the same key value on all instances in the network.

For script help execute with the --help parameter.


Please note that panic_bcast is a beta and more sophisticated ways to prevent cold boot attacks are planned. You can view these plans by searching for the word "TODO" in the source code.

Remember kids: there's no home for swap in opsec.
