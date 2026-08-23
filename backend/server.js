require("dotenv").config();

const express = require("express");
const cors = require("cors");

const app = express();

const taskRoutes = require("./routes/taskRoutes");

app.use(cors());
app.use(express.json());

app.use("/tasks", taskRoutes);

app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "Task Management Backend is Running..."
    });
});

const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
    console.log(`✅ Server running at http://localhost:${PORT}`);
});

server.on("close", () => {
    console.log("❌ HTTP SERVER CLOSED");
});

server.on("error", (error) => {
    console.error("❌ SERVER ERROR:", error);
});

process.on("exit", (code) => {
    console.log("⚠️ NODE PROCESS EXITING WITH CODE:", code);
});

process.on("uncaughtException", (error) => {
    console.error("❌ UNCAUGHT EXCEPTION:", error);
});

process.on("unhandledRejection", (error) => {
    console.error("❌ UNHANDLED REJECTION:", error);
});