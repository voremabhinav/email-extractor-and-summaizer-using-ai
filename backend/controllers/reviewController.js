const reviewService = require("../services/reviewService");

// Get pending projects
const getPendingProjects = async (req, res) => {
    try {
        const projects = await reviewService.getPendingProjects();

        res.status(200).json({
            success: true,
            message: "Pending projects fetched successfully",
            data: projects
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

// Get project by ID
const getProjectById = async (req, res) => {
    try {
        const project = await reviewService.getProjectById(req.params.id);

        res.status(200).json({
            success: true,
            message: "Project fetched successfully",
            data: project
        });

    } catch (error) {
        res.status(404).json({
            success: false,
            message: error.message
        });
    }
};

// Create review
const createReview = async (req, res) => {
    try {
        const {
            project_id,
            reviewer_name,
            technical_comments,
            estimated_days,
            priority,
            review_status
        } = req.body;

        if (!project_id || !reviewer_name) {
            return res.status(400).json({
                success: false,
                message: "project_id and reviewer_name are required"
            });
        }

        const review = await reviewService.createReview({
            project_id,
            reviewer_name,
            technical_comments,
            estimated_days,
            priority,
            review_status
        });

        res.status(201).json({
            success: true,
            message: "Review created successfully",
            data: review
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

// Update review
const updateReview = async (req, res) => {
    try {
        const review = await reviewService.updateReview(
            req.params.id,
            req.body
        );

        res.status(200).json({
            success: true,
            message: "Review updated successfully",
            data: review
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

// Approve project
const approveProject = async (req, res) => {
    try {
        const project = await reviewService.approveProject(
            req.params.id
        );

        res.status(200).json({
            success: true,
            message: "Project approved successfully",
            data: project
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

// Reject project
const rejectProject = async (req, res) => {
    try {
        const project = await reviewService.rejectProject(
            req.params.id
        );

        res.status(200).json({
            success: true,
            message: "Project rejected successfully",
            data: project
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

module.exports = {
    getPendingProjects,
    getProjectById,
    createReview,
    updateReview,
    approveProject,
    rejectProject
};