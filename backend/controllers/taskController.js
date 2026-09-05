const supabase = require("../config/supabaseClient");

// ==========================================
// CREATE / ASSIGN TASK
// ==========================================

const createTask = async (req, res) => {
    try {
        const {
            project_id,
            task_title,
            description,
            assigned_to,
            assigned_by,
            priority,
            deadline
        } = req.body;

        if (
            !project_id ||
            !task_title ||
            !assigned_to ||
            !assigned_by ||
            !priority ||
            !deadline
        ) {
            return res.status(400).json({
                success: false,
                message: "project_id, task_title, assigned_to, assigned_by, priority and deadline are required"
            });
        }

        const { data, error } = await supabase
            .from("tasks")
            .insert([
                {
                    project_id,
                    task_title,
                    description: description || null,
                    assigned_to,
                    assigned_by,
                    priority,
                    status: "Assigned",
                    deadline
                }
            ])
            .select()
            .single();

        if (error) {
            return res.status(500).json({
                success: false,
                message: error.message
            });
        }

        res.status(201).json({
            success: true,
            message: "Task assigned successfully",
            data
        });

    } catch (error) {
        console.error("Create Task Error:", error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};


// ==========================================
// GET ALL TASKS
// ==========================================

const getAllTasks = async (req, res) => {
    try {
        const { data, error } = await supabase
            .from("tasks")
            .select("*")
            .order("created_at", {
                ascending: false
            });

        if (error) {
            return res.status(500).json({
                success: false,
                message: error.message
            });
        }

        res.json({
            success: true,
            message: "All tasks fetched successfully",
            data
        });

    } catch (error) {
        console.error("Get Tasks Error:", error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};


// ==========================================
// GET EMPLOYEE TASKS
// ==========================================

const getEmployeeTasks = async (req, res) => {
    try {
        const { employeeId } = req.params;

        const { data, error } = await supabase
            .from("tasks")
            .select("*")
            .eq("assigned_to", employeeId)
            .order("deadline", {
                ascending: true
            });

        if (error) {
            return res.status(500).json({
                success: false,
                message: error.message
            });
        }

        res.json({
            success: true,
            message: "Employee tasks fetched successfully",
            data
        });

    } catch (error) {
        console.error("Employee Tasks Error:", error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};


// ==========================================
// UPDATE TASK
// ==========================================

const updateTask = async (req, res) => {
    try {
        const { id } = req.params;

        const {
            task_title,
            description,
            assigned_to,
            priority,
            status,
            deadline
        } = req.body;

        const { data, error } = await supabase
            .from("tasks")
            .update({
                task_title,
                description,
                assigned_to,
                priority,
                status,
                deadline
            })
            .eq("id", id)
            .select()
            .single();

        if (error) {
            return res.status(500).json({
                success: false,
                message: error.message
            });
        }

        res.json({
            success: true,
            message: "Task updated successfully",
            data
        });

    } catch (error) {
        console.error("Update Task Error:", error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};


module.exports = {
    createTask,
    getAllTasks,
    getEmployeeTasks,
    updateTask
};