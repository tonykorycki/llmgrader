console.log("UI loaded.");
let loadedData = null;


document.getElementById("send-chat").onclick = function () {
    const input = document.getElementById("chat-input");
    const history = document.getElementById("chat-history");

    if (input.value.trim() !== "") {
        const msg = document.createElement("div");
        msg.textContent = "You: " + input.value;
        history.appendChild(msg);
        input.value = "";
        history.scrollTop = history.scrollHeight;
    }
};

document.getElementById("grade-button").onclick = function () {
    const status = document.getElementById("grade-status"); 

    // Dummy toggle for now
    if (status.classList.contains("status-not-graded")) {
        status.textContent = "Correct";
        status.className = "status-correct";
    } else if (status.classList.contains("status-correct")) {
        status.textContent = "Incorrect";
        status.className = "status-incorrect";
    } else {
        status.textContent = "Not graded";
        status.className = "status-not-graded";
    }
};

document.getElementById("load-file").onclick = function () {
    const fileInput = document.getElementById("solution-file");
    if (!fileInput.files.length) {
        console.log("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/load_file", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())  
    .then(data => {
        if (data.error) {
            console.error("Server error:", data.error);
            return;
        }
  
        // Validate structure
        if (!data.questions || !data.solutions || !data.grading_notes) {
            console.error("Malformed data:", data);
            return;
        }

        const dropdown = document.getElementById("question-number");
       
        // Clear any old options
        dropdown.innerHTML = "";

        // Populate with new options
        for (let i = 0; i < data.num_items; i++) {
            const opt = document.createElement("option");
            opt.value = i;                     // index of the question
            opt.textContent = `Question ${i+1}`; // what the user sees
            dropdown.appendChild(opt);
        }

        // Initially select the first question
        dropdown.selectedIndex = 0;

        // Store parsed data for later use
        loadedData = data;
        
        // Populate fields for the first question
        document.getElementById("question-text").textContent = data.questions[0];
        document.getElementById("ref-solution").textContent = data.solutions[0];
        document.getElementById("grading-notes").textContent = data.grading_notes[0];


    });

};

document.getElementById("question-number").onchange = function () {
    const idx = Number(this.value);
    const data = loadedData;

    if (!data) {
        console.log("No data loaded yet");
        return;
    }

    document.getElementById("ref-solution").textContent = data.solutions[idx];
    document.getElementById("grading-notes").textContent = data.grading_notes[idx];
    document.getElementById("question-text").textContent = data.questions[idx];
};