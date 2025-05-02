// Fetch and render the main menu
async function renderMenu() {
    const menu = document.getElementById("main-menu");
    if (!menu) return;
    const resp = await fetch("/api/operations");
    const ops = await resp.json();
    menu.innerHTML = ops.map(op =>
        `<a href="/operation/${op.operation_id}">${op.name}</a>`
    ).join(" | ");
}
window.addEventListener("DOMContentLoaded", renderMenu);

// Render operation form dynamically
window.renderOperationForm = function(operation) {
    const paramsDiv = document.getElementById("operation-parameters");
    if (!paramsDiv) return;
    paramsDiv.innerHTML = "";
    for (const param of operation.parameters) {
        let inputHtml = "";
        if (param.type === "scalar") {
            inputHtml = `<label>${param.label}: <input type="number" name="${param.name}" step="any"></label>`;
        } else if (param.type === "vector") {
            inputHtml = `<label>${param.label}: <input type="text" name="${param.name}" placeholder="e.g. 1,2,3"></label>`;
        } else if (param.type === "matrix") {
            inputHtml = `<label>${param.label}: <textarea name="${param.name}" rows="3" placeholder="e.g. 1,2;3,4"></textarea></label>`;
        }
        paramsDiv.innerHTML += `<div class="form-row">${inputHtml}</div>`;
    }
    // Attach submit handler
    const form = document.getElementById("operation-form");
    form.onsubmit = async function(e) {
        e.preventDefault();
        const data = {};
        for (const param of operation.parameters) {
            const el = form.elements[param.name];
            if (!el) continue;
            if (param.type === "scalar") {
                data[param.name] = el.value;
            } else if (param.type === "vector") {
                data[param.name] = el.value.split(",").map(Number);
            } else if (param.type === "matrix") {
                // Parse matrix: rows separated by ;, values by ,
                data[param.name] = el.value.split(";").map(row =>
                    row.split(",").map(Number)
                );
            }
        }
        const resultDiv = document.getElementById("operation-result");
        resultDiv.innerHTML = "Calculating...";
        try {
            const resp = await fetch(`/api/operations/${operation.operation_id}/calculate`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            const res = await resp.json();
            if (res.success) {
                resultDiv.innerHTML = renderResult(res.result);
            } else {
                resultDiv.innerHTML = `<div class="error">${res.error}</div>`;
            }
        } catch (err) {
            resultDiv.innerHTML = `<div class="error">Error: ${err}</div>`;
        }
    };
};

// Pretty-print result
function renderResult(result) {
    if (typeof result === "object") {
        return `<pre>${JSON.stringify(result, null, 2)}</pre>`;
    }
    return `<div>${result}</div>`;
}