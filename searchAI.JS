import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const API_URL = process.env.REACT_APP_BACKEND_URL;

export default function SearchAI() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/history`)
      .then((res) => res.json())
      .then((data) => setHistory(data.history));
  }, []);

  const handleSearch = async () => {
    if (!query) return;

    setMessages((prev) => [...prev, { type: "user", text: query }]);

    const response = await fetch(`${API_URL}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keyword: query }),
    });

    const data = await response.json();
    setHistory((prev) => [query, ...prev]);

    const resultMessages = data.results.map((res) => ({
      type: "bot",
      text: `**Summary**: ${res.summary}\n **[Read more](${res.url})**`,
    }));

    const relatedMsg = { type: "bot", text: `**Related Topics**: ${data.related_topics.join(", ")}` };

    setMessages((prev) => [...prev, ...resultMessages, relatedMsg]);
    setQuery("");
  };

  return (
    <div className="flex flex-col h-screen p-4 bg-gray-100">
      <h1 className="text-xl font-bold text-center mb-4">AI Web Search</h1>

      <div className="flex-grow overflow-y-auto space-y-4">
        {messages.map((msg, index) => (
          <Card key={index} className={`p-3 ${msg.type === "user" ? "bg-blue-500 text-white" : "bg-white"}`}>
            <CardContent>{msg.text}</CardContent>
          </Card>
        ))}
      </div>

      <div className="p-3 flex items-center space-x-2 bg-white shadow-lg">
        <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask anything..." />
        <Button onClick={handleSearch}>Search</Button>
      </div>
    </div>
  );
}
