const express = require("express");

const router = express.Router();

const {
    getProgress,
    updateProgress
} = require("../controllers/progressController");


// Get progress of a task
router.get("/:taskId", getProgress);


// Update progress of a task
router.put("/:taskId", updateProgress);


module.exports = router;