const {
    getTaskProgress,
    updateTaskProgress
} = require("../services/progressService");


// GET task progress
const getProgress = async (req, res) => {

    try {

        const { taskId } = req.params;

        const task = await getTaskProgress(taskId);

        res.status(200).json({
            success: true,
            message: "Task progress fetched successfully",
            data: task
        });

    } catch (error) {

        res.status(500).json({
            success: false,
            message: error.message
        });

    }
};


// UPDATE task progress
const updateProgress = async (req, res) => {

    try {

        const { taskId } = req.params;
        const { progress, status } = req.body;

        if (progress === undefined) {
            return res.status(400).json({
                success: false,
                message: "Progress is required"
            });
        }

        if (progress < 0 || progress > 100) {
            return res.status(400).json({
                success: false,
                message: "Progress must be between 0 and 100"
            });
        }

        const updatedTask = await updateTaskProgress(
            taskId,
            progress,
            status
        );

        res.status(200).json({
            success: true,
            message: "Task progress updated successfully",
            data: updatedTask
        });

    } catch (error) {

        res.status(500).json({
            success: false,
            message: error.message
        });

    }
};


module.exports = {
    getProgress,
    updateProgress
};

