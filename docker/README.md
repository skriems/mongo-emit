Setup MongoDB with Docker
=========================

replicaset
----------

    $ docker-compose up -d
    $ ./init.sh

sharded
-------

It's a little more complicated here.

    $ docker-compose up -d
    $ ./init.sh

I've added an [Arbiter][] for each shard which needs to be added to the replicaset on each shard's PRIMARY. I tried to automate it in the `init.sh` but it wasn't reliable.

Let's assume `sh1a` is the Master of the first shard:

    mongo --port 27001 --eval "rs.addArb('sh1Arb:27005')"

And for the second shard:

    mongo --port 27002 --eval "rs.addArb('sh1Arb:27006')"

Now you can connect to the router via

    mongo

#### Cleanup

The data (but also the config) is persistently stored in docker volumes. If you want to start all over don't forget to

    docker volume prune


[Arbiter]: https://docs.mongodb.com/manual/core/replica-set-arbiter/
