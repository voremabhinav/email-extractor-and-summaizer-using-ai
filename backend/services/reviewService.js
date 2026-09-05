const supabase = require("../config/supabaseClient");

// Get projects waiting for senior developer review
const getPendingProjects = async () => {
    const { data, error } = await supabase
        .from("projects")
        .select("*")
        .eq("status", "Pending Review")
        .order("created_at", { ascending: false });

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

// Get one project by ID
const getProjectById = async (id) => {
    const { data, error } = await supabase
        .from("projects")
        .select("*")
        .eq("id", id)
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

// Create a senior developer review
const createReview = async (reviewData) => {
    const { data, error } = await supabase
        .from("project_reviews")
        .insert([reviewData])
        .select()
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

// Update a review
const updateReview = async (id, reviewData) => {
    const { data, error } = await supabase
        .from("project_reviews")
        .update(reviewData)
        .eq("id", id)
        .select()
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

// Approve project
const approveProject = async (projectId) => {
    const { data, error } = await supabase
        .from("projects")
        .update({
            status: "Approved"
        })
        .eq("id", projectId)
        .select()
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

// Reject project
const rejectProject = async (projectId) => {
    const { data, error } = await supabase
        .from("projects")
        .update({
            status: "Rejected"
        })
        .eq("id", projectId)
        .select()
        .single();

    if (error) {
        throw new Error(error.message);
    }

    return data;
};

module.exports = {
    getPendingProjects,
    getProjectById,
    createReview,
    updateReview,
    approveProject,
    rejectProject
};