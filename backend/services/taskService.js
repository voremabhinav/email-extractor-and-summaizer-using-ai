const { supabase } = require("../config/supabaseClient");


// Create a new task
const createTask = async (taskData) => {
    const { data, error } = await supabase
        .from("tasks")
        .insert([taskData])
        .select()
        .single();

    if (error) {
        throw error;
    }

    return data;
};


// Get tasks assigned to an employee
const getTasksByEmployee = async (employeeId) => {
    const { data, error } = await supabase
        .from("tasks")
        .select("*")
        .eq("assigned_to", employeeId)
        .order("created_at", { ascending: false });

    if (error) {
        throw error;
    }

    return data;
};


// Update task status
const updateTaskStatus = async (taskId, status) => {
    const { data, error } = await supabase
        .from("tasks")
        .update({ status })
        .eq("id", taskId)
        .select()
        .single();

    if (error) {
        throw error;
    }

    return data;
};


module.exports = {
    createTask,
    getTasksByEmployee,
    updateTaskStatus
};