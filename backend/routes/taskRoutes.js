const express = require("express");

const {
    createTask,
    getAllTasks,
    getEmployeeTasks,
    updateTask
} = require("../controllers/taskController");

const router = express.Router();

router.post("/", createTask);

router.get("/", getAllTasks);

router.get("/employee/:employeeId", getEmployeeTasks);

router.put("/:id", updateTask);

module.exports = router;