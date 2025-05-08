// Sidebar and burger menu logic
function openSidebar() {
    const sidebar = document.getElementById("sidebar-menu");
    const overlay = document.getElementById("overlay");
    if (sidebar) sidebar.setAttribute("aria-hidden", "false");
    if (overlay) overlay.style.display = "block";
    document.body.style.overflow = "hidden";
}

function closeSidebar() {
    const sidebar = document.getElementById("sidebar-menu");
    const overlay = document.getElementById("overlay");
    if (sidebar) sidebar.setAttribute("aria-hidden", "true");
    if (overlay) overlay.style.display = "none";
    document.body.style.overflow = "";
}

function setupBurgerMenu() {
    const burgerBtn = document.getElementById("burger-menu-btn");
    const closeBtn = document.getElementById("close-sidebar-btn");
    const overlay = document.getElementById("overlay");
    if (burgerBtn) burgerBtn.onclick = openSidebar;
    if (closeBtn) closeBtn.onclick = closeSidebar;
    if (overlay) overlay.onclick = closeSidebar;

    // Accessibility: close on Escape
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape") closeSidebar();
    });
}

// Fetch and render the sidebar menu
async function renderSidebarMenu() {
    const menu = document.getElementById("main-menu");
    if (!menu) return;
    const resp = await fetch("/api/operations");
    const ops = await resp.json();
    menu.innerHTML = ops.map(op =>
        `<a href="/operation/${op.operation_id}" onclick="closeSidebar()">${op.name}</a>`
    ).join("");
}

window.addEventListener("DOMContentLoaded", () => {
    setupBurgerMenu();
    renderSidebarMenu();
    setupCommentForm();
    fetchComments();
});

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
                resultDiv.innerHTML = "Rendering..."
                const rendered = await renderResult(operation.operation_id, res.result);
                resultDiv.innerHTML = rendered;
            } else {
                resultDiv.innerHTML = `<div class="error">${res.error}</div>`;
            }
        } catch (err) {
            resultDiv.innerHTML = `<div class="error">Error: ${err}</div>`;
        }
    };
};

// Render result using server-side rendering functionality
async function renderResult(operationId, result) {
    try {
        const response = await fetch(`/api/renderings/${operationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ result })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch rendering');
        }

        const data = await response.json();
        if (data.success) {
            return `<div>${data.rendered_output}</div>`;
        } else {
            throw new Error(data.error || 'Rendering error');
        }
    } catch (error) {
        console.error('Error rendering result:', error);
        // Fallback to default JSON pretty-printing
        if (typeof result === "object") {
            return `<pre>${JSON.stringify(result, null, 2)}</pre>`;
        }
        return `<div>${result}</div>`;
    }
}

// --- Comment Functionality ---

function renderComments(comments) {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;
    commentsList.innerHTML = comments.map(comment =>
        `<div class="comment">${comment}</div>`
    ).join('');
}

// Submit comment via AJAX and update comment list
function setupCommentForm() {
    const form = document.querySelector('.comments-section form');
    if (!form) return;
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const textarea = form.querySelector('textarea[name="comment"]');
        if (!textarea) return;
        const comment = textarea.value;
        if (!comment) return;
        
        try {
            const resp = await fetch('/api/submit-comment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ comment })
            });
            const data = await resp.json();
            if (data.success) {
                fetchComments();
                textarea.value = '';
            } else {
                throw new Error(data.error || 'Failed to submit comment');
            }
        } catch (err) {
            console.error('Comment submission error:', err);
            alert('Failed to submit comment.');
        }
    });
}

// Fetch comments for the current page/operation
async function fetchComments() {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;
    
    try {
        const resp = await fetch(`/api/comments`);
        const data = await resp.json();
        if (data.success) {
            renderComments(data.comments);
        }
    } catch (err) {
        console.error('Error fetching comments:', err);
        commentsList.innerHTML = '<div class="error">Failed to load comments</div>';
    }
}
