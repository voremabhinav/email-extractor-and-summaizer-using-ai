const supabase = require("../config/supabaseClient");

// Get progress of a particular task
const getTaskProgress = async (taskId) => {
    const { data, error } = await supabase
        .from("tasks")
        .select("*")
        .eq("id", taskId)
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};


// Update task progress
const updateTaskProgress = async (taskId, progress, status) => {

    const updateData = {
        progress: progress
    };

    if (status) {
        updateData.status = status;
    }

    const { data, error } = await supabase
        .from("tasks")
        .update(updateData)
        .eq("id", taskId)
        .select()
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};


module.exports = {
    getTaskProgress,
    updateTaskProgress
};