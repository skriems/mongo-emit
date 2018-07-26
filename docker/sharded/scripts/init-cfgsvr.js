rs.initiate(
   {
      _id: "cfgsvr",
      configsvr: true,
      version: 1,
      members: [
         { _id: 0, host : "config1:27019" },
         { _id: 1, host : "config2:27020" },
      ]
   }
)
