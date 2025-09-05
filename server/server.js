const express = require('express')
const cors = require('cors')
const app = express()
const port = 5000
const path = require("path")

app.use(cors())   // 👈 enable CORS for all routes
app.use(express.json())
app.use(express.static(path.join(__dirname, "public")))

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "views"))

app.get('/', (req, res) => {
  res.render("test")
})

app.get('/data', (req, res) => {
  res.json({
    data: "this is data",
    other: "other thing"
  })
})

app.post("/api/params", (req, res) => {
  const { alpha, epsilon, gamma } = req.body
  console.log("Received Params:", req.body)

  res.json({
    message: "Parameters received successfully",
    alpha,
    epsilon,
    gamma
  })
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
