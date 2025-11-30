// Store the tasks added manually
let tasks = [];

// Handle form submit
document.getElementById("taskForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const id = document.getElementById("id").value.trim();
    const title = document.getElementById("title").value.trim();
    const due_date = document.getElementById("due_date").value;
    const hours = document.getElementById("hours").value;
    const importance = document.getElementById("importance").value;
    const depText = document.getElementById("dependencies").value;

    const dependencies = depText
        ? depText.split(",").map(d => d.trim()).filter(Boolean)
        : [];

    // Create task object
    const newTask = {
        id,
        title,
        due_date: due_date || null,
        estimated_hours: hours ? parseFloat(hours) : 4,
        importance: importance ? parseInt(importance) : 5,
        dependencies
    };

    tasks.push(newTask);

    alert("Task added!");

    // Reset form
    document.getElementById("taskForm").reset();
});


// Handle Analyze button click
document.getElementById("analyzeBtn").addEventListener("click", async function () {
    let finalTasks = [...tasks];

    // If JSON is pasted
    const rawJSON = document.getElementById("jsonInput").value.trim();
    if (rawJSON) {
        try {
            const parsed = JSON.parse(rawJSON);
            if (Array.isArray(parsed)) {
                finalTasks = finalTasks.concat(parsed);
            } else {
                alert("JSON must be an array of tasks!");
                return;
            }
        } catch (err) {
            alert("Invalid JSON!");
            return;
        }
    }

    if (finalTasks.length === 0) {
        alert("Please add tasks before analyzing!");
        return;
    }

    const selectedMode = document.getElementById("mode").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/?mode=" + selectedMode, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(finalTasks),
        });

        const data = await response.json();

        displayResults(data.tasks);
    } catch (error) {
        alert("Error connecting to backend!");
        console.log(error);
    }
});


// Function to show results on page
function displayResults(list) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    list.forEach(task => {
        const box = document.createElement("div");
        box.className = "taskBox";

        box.innerHTML = `
            <h3>${task.title} <small>(${task.id})</small></h3>
            <p><strong>Score:</strong> ${task.score}</p>
            <p><strong>Reasons:</strong> ${task.reasons.join(", ") || "Balanced priority"}</p>
            <p><strong>Due:</strong> ${task.due_date || "None"}</p>
            <p><strong>Hours:</strong> ${task.estimated_hours}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
        `;

        resultDiv.appendChild(box);
    });
}
