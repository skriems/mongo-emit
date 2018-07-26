rs.initiate(
   {
      _id: "sh1",
      version: 1,
      members: [
         { _id: 0, host : "sh1a:27001" },
         { _id: 1, host : "sh1b:27003" },
      ]
   }
)
