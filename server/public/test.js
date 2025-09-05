document.getElementById("send_params").onclick = () => {
  const size = parseFloat(document.getElementById("size").value)
  const alpha = parseFloat(document.getElementById("alpha").value)
  const epsilon = parseFloat(document.getElementById("epsilon").value)
  const gamma = parseFloat(document.getElementById("gamma").value)
  const episodes = parseFloat(document.getElementById("episodes").value)
  const restricted = parseFloat(document.getElementById("restricted").value)

  axios.post("http://localhost:3000/train", {
    size,
    alpha,
    epsilon,
    gamma, 
    episodes,
     restricted
  })
  .then(response => {
    console.log("Server Response:", response.data)
    document.getElementById("response").innerText = JSON.stringify(response.data, null, 2)
  })
  .catch(error => {
    console.error("Error:", error)
  })
}
