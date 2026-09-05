const express = require("express");

const router = express.Router();

const {
    getPendingProjects,
    getProjectById,
    createReview,
    updateReview,
    approveProject,
    rejectProject
} = require("../controllers/reviewController");

// Get all projects waiting for review
router.get("/pending", getPendingProjects);

// Get project by ID
router.get("/:id", getProjectById);

// Create review
router.post("/", createReview);

// Update review
router.put("/:id", updateReview);

// Approve project
router.post("/:id/approve", approveProject);

// Reject project
router.post("/:id/reject", rejectProject);

module.exports = router;