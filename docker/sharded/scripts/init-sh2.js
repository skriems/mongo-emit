rs.initiate(
   {
      _id: "sh2",
      version: 1,
      members: [
         { _id: 0, host : "sh2a:27002" },
         { _id: 1, host : "sh2b:27004" },
      ]
   }
)
