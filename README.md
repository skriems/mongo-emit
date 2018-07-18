mongo-emit
==========

> utility for dumping the new MongoDB [ChangeStreams][]

Info
----

You will receive [ChangeEvents][] which look like::

    {
       _id : { <BSON Object> },
       "operationType" : "<operation>",
       "fullDocument" : { <document> },
       "ns" : {
          "db" : "<database>",
          "coll" : "<collection"
       },
       "documentKey" : { "_id" : <ObjectId> },
       "updateDescription" : {
          "updatedFields" : { <document> },
          "removedFields" : [ "<field>", ... ]
       }
       "clusterTime" : <Timestamp>,
       "txnNumber" : <NumberLong>,
       "lsid" : {
          "id" : <UUID>,
          "uid" : <BinData>
       }
    }

Note that you won't get the full document for `update` operations unless you provide a kwarg to the underlying `watch()` method. Checkout the Configiguration section for further info. In most cases though, it might be suffice to use the `updateDescription` field which is available on `update` operations.


ChangeStream Output
-------------------

You have some of the [pipeline][] stages of the aggregation framework available to
filter the output. Try out the following:

    { "$match" :{ "fullDocument.my_field": <value> } }
    { "$match" :{ "updateDescription.updatedFields.my_field": <value> } }

You can provide those either via the CLI, yaml files or environmental
variables:

    $ mongo-emit --pipeline '{"$match":{"fullDocument.my_field": <value>}}'
    $ STREAM_PIPELINE='{"$match":{"fullDocument.my_field": <value>}}' mongo-emit

Resuming
--------

`mongo-emit` implements a small wrapper Class which stores the `resume_token` while iterating over the returned `cursor` object from the `watch()` method. Simply call the `resume()` method or provide a custom `resume_token`. You can also start at a specific `timestamp` given that it's available in the Oplog.

Configiguration
---------------
You can configure `mongo-emit` in several ways. Keep in mind that the precedence is: `CLI` -> `ENV` -> `YAML` -> `DEFAULTS`. 

Here's a sample configuration file:

    debug: true
    mongo:
      host: localhost
      port: 30001
    stream:
      target: test.users
      options:
        full_document: updateLookup
        # you can either have one of the following
        start_at_operation_time: 2018-07-19T18:00:00
        resume_after: {'_data': '<very_long_token_id>'}
      pipeline:
        - {$match: {updateDescription.updatedFields.exit_status: 1}}

You can overwrite any of those values with environmental variables and use underscores to access any member in this dictionary:

    CONFIG_YAML=./config.yaml MONGO_HOST=my.mongo.example mongo-pub

which would make the proc connect to `my.mongo.example` instead.

Available config options in the `CLI` are:

    usage: mongo-emit [-h] [--target TARGET] [--pipeline PIPELINE]
                         [--resume-token RESUME_TOKEN] [--starttime STARTTIME]
                         [--full-document]

    optional arguments:
      -h, --help            show this help message and exit
      --target TARGET       '<db>' or '<db>.<collection>' to be watched
      --pipeline PIPELINE   aggreate pipeline (list) wrapped in 'single quotes'!
      --resume-token RESUME_TOKEN
                            specify a specific resume_token
      --starttime STARTTIME
                            start at <iso8601_datetime_string>
      --full-document       fullDocument field on _update_ events

Testing
-------

There's a `docker-compose.yml` file which spawns 3 MongoDB containers. User the
`cluster/init.sh` script to initialize the replication:

    $ docker-compose up -d
    $ ./cluster/init.sh

The `mongo1` container becomes the primary and the other two container become
the secondary nodes. Connect to either of them using i.e `mongo --port
30001`, create the DB's, Collections and Documents you want to test with and
then connect `mongo-emit`. You can connect to a DB or Collection:

    MONGO_PORT=30001 mongo-emit --target <db>
    MONGO_PORT=30001 mongo-emit --target <db>.<collection>


Development
-----------

Create a `virtualenv` and do a:

    python setup.py develop


[ChangeStreams]: https://docs.mongodb.com/manual/changeStreams/#change-streams
[ChangeEvents]: https://docs.mongodb.com/manual/reference/change-events/
[pipeline]: https://docs.mongodb.com/manual/changeStreams/#modify-change-stream-output
