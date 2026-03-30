import React from "react"
import { useState, useEffect } from "react"
import SalesforceRecordsTable from "./SalesforceRecordsTable.jsx"

const API_URL = "http://localhost:8000/user_query"
const CONFIG_URL = "http://localhost:8000/config"

function App() {
  const [userNlpQuery, setUserNlpQuery] = useState("")
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [llmTarget, setLlmTarget] = useState("Claude")

  useEffect(() => {
    fetch(CONFIG_URL)
      .then((res) => res.json())
      .then((data) => setLlmTarget(data.llm_target))
      .catch(() => {})
  }, [])

  const onSubmit = async (event) => {
    event.preventDefault()
    if (!userNlpQuery.trim()) {
      return
    }
    const currentInput = userNlpQuery
    setMessages((prev) => [...prev, { role: "user", content: currentInput }])
    setUserNlpQuery("")
    setIsLoading(true)
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_nl_request: currentInput })
    })
    const data = await response.json()
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: `[tool: ${data.selected_tool}] ${data.assistant_response}`,
        dataDisplay: data.data_display ?? null,
        records: data.records ?? null,
      }
    ])
    setIsLoading(false)
  }

  return (
    <main className="container">
      <h1>Chat {llmTarget}</h1>
      <section className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <strong>{message.role === "user" ? "Vous" : "Claude"}:</strong>{" "}
            {message.content}
            {message.role === "assistant" &&
              message.dataDisplay === "array" &&
              message.records?.length > 0 && (
                <SalesforceRecordsTable records={message.records} />
              )}
          </div>
        ))}
      </section>
      <form onSubmit={onSubmit} className="composer">
        <input
          value={userNlpQuery}
          onChange={(event) => setUserNlpQuery(event.target.value)}
          placeholder="Ecrivez votre demande"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Envoi..." : "Envoyer"}
        </button>
      </form>
    </main>
  )
}

export default App
